import React, { useState, useEffect } from 'react';
import { requestAPI } from '../../handler';
import { useParams } from 'react-router-dom';
import StyledTabbedHeader from '../common/TabbedHeader';
import StyledWorkflowLaunchPanel from './WorkflowLaunchPanel';
import StyledWorkflowDocsPanel from './WorkflowDocsPanel';
import styled from 'styled-components';
import { Workflow } from './types';
import { Nullable } from 'tsdef';

// -----------------------------------------------------------------------------
// Helper methods
// -----------------------------------------------------------------------------
const getWorkflowData = async (name: string): Promise<Workflow> => {
  return await requestAPI<any>(`workflows/${name}`);
};

const getInstanceParams = async (instance_id: string) => {
  const { path } = await requestAPI<any>(`instances/${instance_id}`);
  const encodedPath = encodeURIComponent(`${path}/params.json`);
  const { exists, contents } = await requestAPI<any>(
    `file/${encodedPath}?contents=true`
  );
  if (!exists) {
    return null;
  }
  return JSON.parse(contents.join(''));
};

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface IWorkflowComponent {
  className?: string;
}

const WorkflowComponent = ({ className }: IWorkflowComponent): JSX.Element => {
  // ------------------------------------
  // Initialise state
  // ------------------------------------
  const params = useParams();
  const workflowName = params.name as string;
  const instanceId = params.instance_id || null;
  const [selectedTab, setSelectedTab] = useState(0);
  const [workflowData, setWorkflowData] = useState<Nullable<Workflow>>(null);
  const [animationClass, setAnimationClass] = useState('animated');

  useEffect(() => {
    const getData = async () => {
      // We set workflow data after getting it from the API
      const data = await getWorkflowData(params.name as string);
      // But if an instanceId is specified, we use the parameter
      // values from that instance run instead
      if (instanceId) {
        setWorkflowData({
          ...data,
          defaults: {
            ...data.defaults,
            ...((await getInstanceParams(instanceId)) || {})
          }
        });
      } else {
        setWorkflowData(data);
      }
    };
    getData();
  }, [params]);

  // ------------------------------------
  // Handle missing data
  // ------------------------------------
  if (!workflowData) {
    return <React.Fragment></React.Fragment>;
  }

  // ------------------------------------
  // Tabbed interface
  // ------------------------------------
  const tabs = [
    {
      body: 'Launch workflow',
      onClick: () => setSelectedTab(0),
      element: (
        <div
          className={`tab-contents ${animationClass}`}
          onAnimationEnd={() => setAnimationClass('')}
        >
          <StyledWorkflowLaunchPanel
            workflowName={workflowName}
            workflowSchema={workflowData?.schema}
            workflowDefaults={workflowData?.defaults || {}}
          />
        </div>
      )
    },
    {
      body: 'Documentation',
      onClick: () => setSelectedTab(1),
      element: (
        <div className="tab-contents animated">
          <StyledWorkflowDocsPanel docs={workflowData?.docs} />
        </div>
      )
    }
  ];

  return workflowData ? (
    <div className={`workflow ${className}`}>
      <div className="workflow-container">
        <StyledTabbedHeader
          title={workflowData.name}
          body={<p className="large">{workflowData.desc}</p>}
          active={selectedTab}
          tabs={tabs}
        />
        {tabs[selectedTab].element}
      </div>
    </div>
  ) : (
    <React.Fragment />
  );
};

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledWorkflowComponent = styled(WorkflowComponent)`
  background-color: #f6f6f6;

  .workflow-container {
    box-sizing: border-box;
    padding: 0 0 50px 0 !important;
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
    width: 100%;
    padding: 0 25px 0 25px;
    box-sizing: border-box;
    margin: 0 auto 25px auto;
  }

  .animated {
    opacity: 0;
    animation-name: fadeInUp;
    animation-duration: 1s;
    animation-fill-mode: both;
  }
`;

export default StyledWorkflowComponent;
