import React, { useState, useEffect, SetStateAction, Dispatch } from 'react';
import { useNavigate } from 'react-router-dom';
import StyledWorkflowParameterSection from './WorkflowParameterSection';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { WorkflowSchema } from './types';
import { requestAPI } from '../../handler';
import { Nullable, AnyObject } from 'tsdef';
import styled from 'styled-components';
import {
  validateSchema,
  getSchemaSections,
  groupErrorsByParam
} from './schema';
import {
  faCheckCircle,
  faTimesCircle
} from '@fortawesome/free-solid-svg-icons';

// -----------------------------------------------------------------------------
// Global state
// -----------------------------------------------------------------------------
type BrowserCtx = {
  browserLocation: Nullable<string>;
  setBrowserLocation: Dispatch<SetStateAction<Nullable<string>>>;
};

const initialBrowserCtx: BrowserCtx = {
  browserLocation: null,
  setBrowserLocation: (): void => {
    throw new Error('setBrowserLocation function must be overridden');
  }
};

export const BrowserContext = React.createContext<BrowserCtx>(
  initialBrowserCtx
);

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface IWorkflowLaunchPanel {
  className?: string;
  workflowName: string;
  workflowSchema: WorkflowSchema;
  workflowDefaults: AnyObject;
}

const WorkflowLaunchPanel = ({
  className,
  workflowName,
  workflowSchema,
  workflowDefaults
}: IWorkflowLaunchPanel): JSX.Element => {
  // ------------------------------------
  // Initialise state
  // ------------------------------------
  const navigate = useNavigate();

  // Parameters
  const paramSections: AnyObject[] = getSchemaSections(workflowSchema);
  const [instParams, setInstParams] = useState<AnyObject>(workflowDefaults);

  // Validation
  const [isValid, setIsValid] = useState(false);
  const [valErrors, setValErrors] = useState<AnyObject>({});

  // Instance Create
  const [instanceName, setInstanceName] = useState<Nullable<string>>();
  const [instNameError, setInstNameError] = useState<Nullable<string>>();
  const [instCreateError, setInstCreateError] = useState<Nullable<string>>();

  // File Browser
  const [browserLocation, setBrowserLocation] = useState<Nullable<string>>(
    null
  );

  // ------------------------------------
  // Handle parameter validation
  // ------------------------------------
  const validateParams = (params: AnyObject) => {
    const { valid, errors } = validateSchema(params, workflowSchema);
    setValErrors(valid ? {} : groupErrorsByParam(errors));
    setIsValid(valid);
  };

  useEffect(() => {
    validateParams(instParams);
  }, [instParams]);

  const handleInputChange = (id: string, value: any) => {
    if (value === '') {
      setInstParams(instParams => {
        const { [id]: _, ...rest } = instParams;
        return rest;
      });
      return;
    }
    setInstParams(instParams => ({ ...instParams, [id]: value }));
  };

  // ------------------------------------
  // Handle instance naming
  // ------------------------------------
  const namePattern = new RegExp('^[-0-9A-Za-z_ ]+$');
  const handleInstanceRename = (name: string) => {
    if (name === '') {
      setInstanceName(null);
      setInstNameError('An instance name cannot be empty');
      return;
    }
    if (!namePattern.test(name)) {
      setInstanceName(null);
      setInstNameError(
        'An instance name can only contain dashes, ' +
          'underscores, spaces, letters and numbers'
      );
      return;
    }
    setInstanceName(name);
    setInstNameError(null);
  };

  // ------------------------------------
  // Handle workflow launch
  // ------------------------------------
  const launchWorkflow = async () => {
    if (!isValid || !instanceName) {
      return;
    }
    const { created, instance, error } = await requestAPI<any>('instances', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        workflow: workflowName,
        params: instParams,
        ...(instanceName ? { name: instanceName } : {})
      })
    });
    if (error) {
      setInstCreateError(error);
    }
    if (!created) {
      return;
    }
    navigate(`/instances/${instance.id}`);
  };

  return (
    <div className={`launch-panel ${className}`}>
      {/* Instance name */}
      <div className={`instance-name ${instanceName ? '' : 'invalid'}`}>
        <input
          id="worflow-name-input"
          type="text"
          placeholder={'Name your experiment...'}
          onChange={e => handleInstanceRename(e.target.value)}
          maxLength={50}
        />
        <div
          className={`instance-name-input-errors ${
            instNameError || !instanceName ? 'invalid' : ''
          }`}
        >
          {instNameError || !instanceName ? (
            <FontAwesomeIcon icon={faTimesCircle} />
          ) : (
            <FontAwesomeIcon icon={faCheckCircle} />
          )}
        </div>
      </div>

      {/* Workflow params */}
      <BrowserContext.Provider value={{ browserLocation, setBrowserLocation }}>
        <div className="parameter-sections">
          <ul>
            {paramSections.map((Section, idx) => (
              <li>
                <StyledWorkflowParameterSection
                  title={Section.title}
                  description={Section.description}
                  fa_icon={Section.fa_icon}
                  initOpen={idx ? false : true}
                  properties={Section.properties}
                  defaults={workflowDefaults}
                  errors={valErrors}
                  onChange={handleInputChange}
                />
              </li>
            ))}
          </ul>
        </div>
      </BrowserContext.Provider>

      {/* Workflow launch */}
      <div
        className={`launch-control ${
          isValid && instanceName ? 'active' : 'inactive'
        }`}
      >
        <button onClick={() => launchWorkflow()}>Launch Workflow</button>
        {instCreateError ? (
          <div className="error">
            <p>Error: {instCreateError}</p>
          </div>
        ) : (
          ''
        )}
      </div>
    </div>
  );
};

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledWorkflowLaunchPanel = styled(WorkflowLaunchPanel)`
  && {
    max-width: 1024px;
    padding: 0 0 15px 0;
    margin: 0 auto;
  }

  //
  // Instance naming
  //
  .instance-name {
    position: relative;
  }

  .instance-name input {
    box-sizing: border-box;
    width: 100%;
    margin: 0;
    padding: 25px;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    background-color: white;
    border: none;
    border-radius: 4px;
    outline: none;
    transition: 0.2s ease-in-out all;
  }

  .instance-name.invalid input {
    color: #e34040;
  }

  .instance-name-input-errors {
    position: absolute;
    top: 25px;
    right: 25px;
  }

  .instance-name-input-errors svg {
    width: 18px;
    height: 18px;
    color: #1d9655;
  }

  .instance-name-input-errors.invalid svg {
    color: #e34040;
  }

  //
  // Launch control
  //
  .launch-control {
    margin: 15px 0 0 0;
  }

  .launch-control button {
    box-sizing: border-box;
    width: 100%;
    padding: 25px 25px;
    border: 0;
    text-transform: uppercase;
    font-size: 11px;
    border-radius: 4px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    transition: 0.2s ease-in-out all;
    outline: none;
    cursor: pointer;
  }

  .launch-control.active button {
    border: 1px solid #1d9655;
    background-color: #1d9655;
    color: white;
  }
  .launch-control.active button:hover {
    cursor: pointer;
    background-color: white;
    color: #1d9655;
  }
  .launch-control.error p {
    padding: 15px 0 0 0;
    color: #e34040;
  }
`;

export default StyledWorkflowLaunchPanel;
