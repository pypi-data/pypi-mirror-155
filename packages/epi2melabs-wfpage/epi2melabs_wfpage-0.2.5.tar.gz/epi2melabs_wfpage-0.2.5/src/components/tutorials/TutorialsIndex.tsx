import React, { useState } from 'react';
import styled from 'styled-components';
import StyledHeaderTitle from '../common/TabbedHeader';
import StyledNotebooksList from './TutorialsList';
import { IDocumentManager } from '@jupyterlab/docmanager';

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------

interface ITutorialsPanel {
  className?: string;
  docTrack: IDocumentManager;
  templateDir: string;
  workDir: string;
}

const TutorialsPanel = ({
  className,
  docTrack,
  templateDir,
  workDir
}: ITutorialsPanel): JSX.Element => {
  const [selectedTab, setSelectedTab] = useState(0);

  const handleNotebookClone = async (
    path: string,
    docTrack: IDocumentManager
  ) => {
    await docTrack.copy(path, workDir).then(e => {
      docTrack.open(path);
    });
  };

  const handleNotebookOpen = (path: string, docTrack: IDocumentManager) => {
    docTrack.open(path);
  };

  const tabs = [
    {
      body: 'Select tutorial',
      onClick: () => setSelectedTab(0),
      element: (
        <div className="tab-contents">
          <StyledNotebooksList
            path={templateDir}
            onClick={handleNotebookClone}
            docTrack={docTrack}
            buttonText="Open notebook"
          />
        </div>
      )
    },
    {
      body: 'Tutorials history',
      onClick: () => setSelectedTab(1),
      element: (
        <div className="tab-contents">
          <StyledNotebooksList
            path={workDir}
            onClick={handleNotebookOpen}
            docTrack={docTrack}
            buttonText="Open notebook"
          />
        </div>
      )
    }
  ];

  return (
    <div className={`index-panel ${className}`}>
      <StyledHeaderTitle
        title="EPI2ME Labs Tutorials"
        body={
          <p className="large">
            EPI2ME Labs maintains a growing collection of tutorials on a range
            of topics from basic quality control to genome assembly. These are
            free and open to use by anyone.
          </p>
        }
        active={selectedTab}
        tabs={tabs}
      />

      {tabs[selectedTab].element}
    </div>
  );
};

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledTutorialsPanel = styled(TutorialsPanel)`
  && {
    background-color: #f6f6f6;
    padding-bottom: 50px;
  }

  @keyframes fadeInUp {
    from {
      transform: translate3d(0, 40px, 0);
    }

    to {
      transform: translate3d(0, 0, 0);
      opacity: 1;
    }
  }

  .tab-contents {
    padding: 0 25px;
    opacity: 0;
    animation-name: fadeInUp;
    animation-duration: 1s;
    animation-fill-mode: both;
  }
`;

export default StyledTutorialsPanel;
