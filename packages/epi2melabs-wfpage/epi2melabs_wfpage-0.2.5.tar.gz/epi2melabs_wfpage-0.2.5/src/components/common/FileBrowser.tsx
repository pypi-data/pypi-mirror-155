import React, { useCallback, useEffect, useState } from 'react';
import { ChonkyIconFA } from 'chonky-icon-fontawesome';
import { requestAPI } from '../../handler';
import styled from 'styled-components';
import { Nullable } from 'tsdef';
import {
  ChonkyActions,
  ChonkyFileActionData,
  FileBrowser,
  FileContextMenu,
  FileData,
  FileList,
  FileNavbar,
  FileToolbar
} from 'chonky';

const actionsToDisable: string[] = [
  ChonkyActions.SelectAllFiles.id,
  ChonkyActions.OpenSelection.id,
  ChonkyActions.ClearSelection.id
];

// -----------------------------------------------------------------------------
// Type definitions
// -----------------------------------------------------------------------------
interface IPath {
  name: string;
  path: string;
  updated: string;
  isdir: boolean;
  exists: boolean;
  error: Nullable<string>;
  breadcrumbs: Nullable<string[]>;
}

// interface IFilePath extends IPath {
//   contents?: Nullable<string[]>
// }

interface IDirectoryPath extends IPath {
  contents?: Nullable<IPath[]>;
}

interface IFileBrowser {
  className?: string;
  rootAlias: string;
  rootFolder: string;
  initialFolder: string;
  onSelect: CallableFunction;
  onClose: CallableFunction;
  allowFiles: boolean;
  allowDirectories: boolean;
}

// -----------------------------------------------------------------------------
// Utility methods
// -----------------------------------------------------------------------------
export const getParentDir = (path: string): string => {
  const parent = path.split('/').slice(0, -1).join('/');
  if (parent === '') {
    return '/';
  }
  return parent;
};

// TODO: Abstract this away from this component
export const getDir = async (path: string): Promise<IDirectoryPath> => {
  const encodedPath = encodeURIComponent(path);
  return await requestAPI<any>(`directory/${encodedPath}?contents=true`, {
    method: 'GET'
  });
};

// -----------------------------------------------------------------------------
// Chonky/Redux Action Handlers
// -----------------------------------------------------------------------------
export const useFileActionHandler = (
  setCurrentFolder: (folderId: string) => void,
  setCurrentSelection: (selection: string | null) => void,
  allowFiles: boolean,
  allowDirectories: boolean
): ((data: ChonkyFileActionData) => void) => {
  return useCallback(
    (data: ChonkyFileActionData) => {
      // Change directory
      if (data.id === ChonkyActions.OpenFiles.id) {
        const { targetFile, files } = data.payload;
        const fileToOpen = targetFile ?? files[0];
        if (fileToOpen && fileToOpen.isDir) {
          setCurrentFolder(fileToOpen.id);
          setCurrentSelection(null);
          return;
        }
      }
      // Change selection
      if (data.id === ChonkyActions.MouseClickFile.id) {
        const { file } = data.payload;
        if (allowDirectories && file.isDir) {
          setCurrentSelection(file.path);
          return;
        }
        if (allowFiles && !file.isDir) {
          setCurrentSelection(file.path);
          return;
        }
        return;
      }
    },
    [setCurrentFolder, setCurrentSelection]
  );
};

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
const ReadOnlyFileBrowser = ({
  className,
  onSelect,
  onClose,
  rootAlias,
  rootFolder,
  initialFolder,
  allowFiles,
  allowDirectories
}: IFileBrowser) => {
  // ------------------------------------
  // Set up state
  // ------------------------------------
  const [files, setFiles] = useState<FileData[]>([]);
  const [folderChain, setFolderChain] = useState<FileData[]>([]);
  const [currentFolder, setCurrentFolder] = useState(initialFolder);
  const [currentSelection, setCurrentSelection] = useState<null | string>(null);
  const handleFileAction = useFileActionHandler(
    setCurrentFolder,
    setCurrentSelection,
    allowFiles,
    allowDirectories
  );

  const rootCrumb = {
    id: rootFolder,
    name: rootAlias,
    path: rootFolder,
    parentId: null,
    isDir: true
  };

  // ------------------------------------
  // Handle browser location changes
  // ------------------------------------
  useEffect(() => {
    // When we change location in the filebrowser,
    // we must update with the contents of the new
    // directory, and also set the breadcrumbs
    const useFiles = async (currentFolderId: string) => {
      const data = await getDir(currentFolderId);
      // This sets the breadcrumbs
      setFolderChain(
        getFolderChain(data.name, data.breadcrumbs || [], rootCrumb)
      );
      // This sets the contents
      if (!data.contents?.length) {
        setFiles([]);
        return;
      }
      const files = data.contents.map((Item: IPath) => ({
        id: Item.path,
        parentId: getParentDir(data.path),
        isDir: Item.isdir,
        ...Item
      }));
      setFiles(files);
    };
    useFiles(currentFolder);
  }, [currentFolder]);

  const getFolderChain = (
    currentFolderName: string,
    breadcrumbs: string[],
    rootCrumb: FileData
  ) => {
    const parseChain = () => {
      const breadcrumbsCurrent = [...breadcrumbs.slice(1), currentFolderName];
      // TODO: this or a reducer?
      let accumulator: string[] = [rootCrumb.path];
      return breadcrumbsCurrent.map(Item => {
        const name = Item.replace('/', '');
        const parent = accumulator.join('/');
        accumulator = [...accumulator, name];
        const path = accumulator.join('/');
        return {
          id: path,
          name: name,
          path: path,
          parentId: parent,
          isDir: true
        };
      });
    };
    return currentFolderName === rootCrumb.path
      ? [rootCrumb]
      : [rootCrumb, ...parseChain()];
  };

  // ------------------------------------
  // Enable or disable select button
  // ------------------------------------
  return (
    <div className={`file-browser ${className}`}>
      <div className="file-browser-container">
        <FileBrowser
          instanceId="core"
          files={files}
          folderChain={folderChain}
          disableDragAndDrop={true}
          onFileAction={handleFileAction}
          iconComponent={ChonkyIconFA}
          disableSelection={true}
          disableDefaultFileActions={actionsToDisable}
        >
          <FileNavbar />
          <FileToolbar />
          <FileList />
          <FileContextMenu />
        </FileBrowser>
        <div className="file-browser-controls">
          <button
            className="file-browser-cancel"
            onClick={() => onClose(currentFolder)}
          >
            Cancel
          </button>
          <button
            className={`${
              currentSelection ? 'active' : ''
            } file-browser-select`}
            onClick={() =>
              currentSelection ? onSelect(currentSelection, currentFolder) : ''
            }
          >
            Select
          </button>
        </div>
      </div>
    </div>
  );
};

const StyledReadOnlyFileBrowser = styled(ReadOnlyFileBrowser)`
  && {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    background-color: rgba(0, 0, 0, 0.2);
    z-index: 2000;
    display: none;
    justify-content: center;
    align-items: center;
  }

  &&.open {
    display: flex;
  }

  .file-browser-container {
    box-sizing: border-box;
    max-width: 90%;
    max-height: 80vh;
    width: 1125px;
    height: 650px;
    padding: 25px;
    display: flex;
    flex-direction: column;
    border-radius: 4px;
    background-color: white;

    .chonky-chonkyRoot {
      color: #fff;
      border: solid 1px transparent;
      height: 100%;
      display: flex;
      padding: 8px;
      font-size: 15px;
      box-sizing: border-box;
      text-align: left;
      font-family: sans-serif;
      user-select: none;
      touch-action: manipulation;
      border-radius: 4px;
      flex-direction: column;
      -ms-user-select: none;
      moz-user-select: none;
      webkit-user-select: none;
      webkit-touch-callout: none;
    }

    .chonky-iconWithText {
      margin-right: 8px;
    }

    .MuiButton-text {
      padding: 6px 8px;
    }

    .chonky-navbarWrapper {
      padding-bottom: 8px;
    }

    .chonky-fileEntryClickableWrapper svg {
      margin: 0 8px;
    }

    .chonky-toolbarLeft {
      display: flex;
      flex-grow: 10000;
      flex-wrap: nowrap;
      padding-bottom: 8px;
    }

    .chonky-toolbarRight {
      display: flex;
      flex-wrap: nowrap;
      padding-bottom: 8px;
    }

    .chonky-searchFieldInputInner {
      height: 26px !important;
      margin: 0;
      padding: 0 8px 0 0 !important;
      font-size: 15px !important;
      line-height: 26px !important;
      -webkit-appearance: none;
    }

    .chonky-searchFieldInput fieldset {
      display: none;
    }

    .MuiInputAdornment-positionStart {
      margin-right: 8px;
    }

    .MuiInputAdornment-root {
      height: 0.01em;
      display: flex;
      max-height: 2em;
      align-items: center;
      white-space: nowrap;
    }
  }

  .file-browser-controls {
    padding: 25px 0 0 0;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: end;
  }

  .file-browser-controls button {
    padding: 10px 24px;
    margin-left: 10px;
    border-radius: 4px;
    border: none;
    font-weight: 500;
    font-size: 13px;
    line-height: 1em;
    transition: 0.2s ease-in-out all;
    background-color: #eee;
  }

  .file-browser-controls button.file-browser-select {
    color: lightgrey;
  }

  .file-browser-controls button.file-browser-cancel {
    cursor: pointer;
  }

  .file-browser-controls button.active {
    background-color: #00485b;
    color: white;
    cursor: pointer;
  }
`;

export default StyledReadOnlyFileBrowser;
