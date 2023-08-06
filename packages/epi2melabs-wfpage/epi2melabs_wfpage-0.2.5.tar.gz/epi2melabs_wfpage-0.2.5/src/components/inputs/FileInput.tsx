import React, {
  useState,
  useRef,
  useEffect,
  useCallback,
  useContext
} from 'react';
import { requestAPI } from '../../handler';
import styled from 'styled-components';
import { debounce } from 'lodash';
import StyledTooltip from '../common/Tooltip';
import StyledReadOnlyFileBrowser, {
  getDir,
  getParentDir
} from '../common/FileBrowser';
import { BrowserContext } from '../workflow/WorkflowLaunchPanel';
import { Nullable } from 'tsdef';

// -----------------------------------------------------------------------------
// Type definitions
// -----------------------------------------------------------------------------
export const FILE_INPUT = 'file';
export const DIR_INPUT = 'dir';
export const PATH_INPUT = 'path';

export interface IFileSettings {
  id: string;
  label: string;
  format: string;
  description?: string;
  help_text?: string;
  defaultValue?: string;
  pattern?: string;
}

interface IFileInput extends IFileSettings {
  className?: string;
  error: string[];
  onChange: CallableFunction;
}

// -----------------------------------------------------------------------------
// Helper methods
// -----------------------------------------------------------------------------
const getNativeValue = (element: any) => element.current.value;

const setNativeValue = (element: any, value: any) => {
  const valueSetter = Object.getOwnPropertyDescriptor(element, 'value')?.set;
  const prototype = Object.getPrototypeOf(element);
  const prototypeValueSetter = Object.getOwnPropertyDescriptor(
    prototype,
    'value'
  )?.set;

  if (valueSetter && valueSetter !== prototypeValueSetter) {
    prototypeValueSetter?.call(element, value);
  } else {
    valueSetter?.call(element, value);
  }
};

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
const FileInput = ({
  id,
  label,
  format,
  description,
  help_text,
  defaultValue,
  pattern,
  error,
  onChange,
  className
}: IFileInput) => {
  // ------------------------------------
  // Set up state
  // ------------------------------------
  const inputRef = useRef(null);
  const [rootFolder, setRootFolder] = useState<Nullable<string>>(null);
  const { browserLocation, setBrowserLocation } = useContext(BrowserContext);
  const [browserError, setBrowserError] = useState<Nullable<string>>(null);
  const [browserOpen, setBrowserOpen] = useState(false);
  const [currentFolder, setCurrentFolder] = useState(
    defaultValue || browserLocation
  );

  useEffect(() => {
    const updateRoot = async () => {
      const root = await getDir('/');
      setRootFolder(root.path);
    };
    updateRoot();
  }, []);

  // ------------------------------------
  // Handle browser change
  // ------------------------------------
  const onBrowserOpen = (ref: any) => {
    const value = getNativeValue(ref);
    const hasValue = !!value;
    if (hasValue) {
      setCurrentFolder(getParentDir(value));
    } else {
      setCurrentFolder(browserLocation);
    }
    setBrowserOpen(true);
  };

  const onBrowserClose = (currentFolder: string) => {
    setCurrentFolder(currentFolder);
    setBrowserLocation(currentFolder);
    setBrowserOpen(false);
  };

  const onBrowserSelect = (
    ref: any,
    currentSelection: string,
    currentFolder: string
  ) => {
    // Update input element
    const current = ref.current;
    if (current) {
      setNativeValue(current, currentSelection);
      const event = new Event('input', { bubbles: true });
      current.dispatchEvent(event);
    }
    setCurrentFolder(currentFolder);
    setBrowserLocation(currentFolder);
    setBrowserOpen(false);
  };

  // ------------------------------------
  // Handle input change
  // ------------------------------------
  const validatePath = async (path: string) => {
    if (
      [/http:\/\//, /https:\/\//, /^$/, /s3:\/\//].some(rx => rx.test(path))
    ) {
      setBrowserError(null);
      onChange(id, path);
      return;
    }
    const encodedPath = encodeURIComponent(path);
    const fmt = format.split('-')[0];
    const data = await requestAPI<any>(`${fmt}/${encodedPath}`, {
      method: 'GET'
    });
    if (!data.exists) {
      setBrowserError(data.error);
      onChange(id, '');
      return;
    }
    setBrowserError(null);
    onChange(id, path);
  };

  const handler = useCallback(debounce(validatePath, 200), []);

  // ------------------------------------
  // Collect errors
  // ------------------------------------
  let errors: string[] = [];
  if (error.length) {
    errors = [...error];
  }
  if (browserError) {
    errors = [browserError, ...errors];
  }

  return (
    <div id={id} className={`file-input ${className}`}>
      <div className="file-input-header">
        <div>
          <h4>{label}</h4>
          {description ? <p>{description}</p> : ''}
        </div>
        {help_text ? (
          <div className="file-input-help">
            <StyledTooltip text={help_text} />
          </div>
        ) : (
          ''
        )}
      </div>
      <div className="file-input-container">
        <label htmlFor={id}>
          <input
            id={id}
            ref={inputRef}
            type="text"
            placeholder={'Enter a value'}
            defaultValue={defaultValue}
            pattern={pattern}
            onChange={e => handler(e.target.value)}
          />
        </label>
        <button
          className="file-browser-toggle"
          onClick={() => (rootFolder ? onBrowserOpen(inputRef) : '')}
        >
          Browse
        </button>
      </div>

      {browserOpen && rootFolder ? (
        <StyledReadOnlyFileBrowser
          onClose={onBrowserClose}
          onSelect={(i: string, j: string) => onBrowserSelect(inputRef, i, j)}
          rootAlias={rootFolder === '/' ? 'Root' : rootFolder}
          rootFolder={rootFolder}
          initialFolder={currentFolder || rootFolder}
          allowFiles={!!['file-path', 'path'].includes(format)}
          allowDirectories={!!['directory-path', 'path'].includes(format)}
        />
      ) : (
        ''
      )}

      {errors.length ? (
        <div className="error">
          {errors.map(Err => (
            <p>Error: {Err}</p>
          ))}
        </div>
      ) : (
        ''
      )}
    </div>
  );
};

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledFileInput = styled(FileInput)`
  h4 {
    padding: 0 0 5px 0;
  }

  p {
    padding: 0 0 10px 0;
  }

  .file-input-container {
    display: flex;
    color: #212529;
    border-radius: 4px;
    border: 1px solid rgba(0, 0, 0, 0.125);
    background-color: #f8f9fa;
  }

  .file-input-container:hover {
    border-color: #005c75;
    box-shadow: 0 0 0 0.25rem rgb(13 110 253 / 25%);
  }

  label {
    width: 100%;
    display: flex;
  }

  input {
    display: block;
    width: 100%;
    box-sizing: border-box;
  }

  input,
  .file-browser-toggle {
    margin: 0;
    padding: 15px 25px;

    font-size: 14px;
    line-height: 1em;

    color: #212529;
    border: 0;
    background-color: transparent;
    border-top-left-radius: 4px;
    border-bottom-left-radius: 4px;
    outline: none;

    transition: 0.2s ease-in-out all;
  }

  .file-browser-toggle {
    line-height: 1.2em;
    border-radius: 0;
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
    background-color: rgba(0, 0, 0, 0.125);
    color: #333;
    cursor: pointer;
  }

  .file-browser-toggle:hover {
    background-color: #005c75;
    color: white;
  }

  .file-browser {
    position: fixed;
    z-index: 10000;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    top: 0px;
    left: 0px;
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.35);
    /* max-height: 300px; */
    /* margin: 10px 0 0 0; */
    /* border-radius: 4px; */
    /* background-color: #f3f3f3; */
    /* overflow-y: auto; */
  }

  .file-browser-contents {
    width: calc(100% - 50px);
    max-width: 900px;
    /* max-height: 500px; */
    border-radius: 4px;
    overflow-y: auto;
    /* background-color: #f3f3f3; */
    background-color: rgba(255, 255, 255, 0.6);
  }

  .file-browser-contents > ul {
    max-height: 500px;
    overflow-y: auto;
  }

  .file-browser-path button {
    box-sizing: border-box;
    width: 100%;
    padding: 15px 25px;
    display: flex;
    align-items: center;
    text-align: left;
    font-size: 12px;
    font-family: monospace;
    letter-spacing: 0.05em;
    outline: none;
    border: none;
    border-radius: 0;
    border-bottom: 1px solid #f4f4f4;
    cursor: pointer;
  }

  .file-browser-path:nth-child(even) button {
    background-color: #f2f2f2;
  }

  .file-browser-path:last-child button {
    border-bottom: none;
  }

  .file-browser-path button:hover {
    color: #005c75;
  }

  .file-browser-path.selected button {
    background-color: #005c75;
    color: white;
  }

  .file-browser-path.selected button:hover {
    color: white;
  }

  .file-browser-back {
    font-style: italic;
    background-color: rgba(0, 0, 0, 0.1);
  }

  .file-browser-close {
    padding: 15px;
    display: flex;
    justify-content: flex-end;
    background-color: white;
  }

  .file-browser-close button {
    padding: 10px 24px;
    border-radius: 4px;
    border: none;
    font-weight: 500;
    font-size: 13px;
    line-height: 1em;
    transition: 0.2s ease-in-out all;
    background-color: #eee;
    cursor: pointer;
  }

  .file-browser-path.file-browser-close:hover button {
    background-color: #f2f2f2;
    color: #333;
  }

  .file-browser-path button svg {
    padding: 0 10px 0 0;
    color: lightgray;
    font-size: 1.5em;
  }

  .file-browser-path button:hover svg {
    color: #005c75;
  }

  .file-browser-path.selected button:hover svg {
    color: lightgray;
  }

  .error p {
    padding: 15px 0 0 0;
    color: #e34040;
  }

  .file-input-header {
    display: flex;
    justify-content: space-between;
  }

  .file-input-help {
    position: relative;
    cursor: pointer;
    display: flex;
    align-items: flex-end;
    padding: 0 0 10px 0;
  }
`;

export default StyledFileInput;
