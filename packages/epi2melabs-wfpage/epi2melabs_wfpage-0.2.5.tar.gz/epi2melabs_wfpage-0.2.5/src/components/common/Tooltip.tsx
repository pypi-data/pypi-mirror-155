import React from 'react';
import styled from 'styled-components';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faQuestionCircle } from '@fortawesome/free-solid-svg-icons';

const Tooltip = ({
  text,
  className
}: {
  className?: string;
  text: string;
}): JSX.Element => (
  <div className={`${className} tooltip`}>
    <FontAwesomeIcon icon={faQuestionCircle} />
    <p>{text}</p>
  </div>
);

const StyledTooltip = styled(Tooltip)`
  && svg {
    width: 18px;
    height: 18px;
    color: rgba(0, 0, 0, 0.3);
  }

  && p {
    display: none;
  }

  &&:hover p {
    max-width: calc(100vw - 250px);
    width: 500px;
    margin-right: 25px;
    padding: 15px;
    display: block;
    position: absolute;
    right: 0;
    top: 0;
    border-radius: 4px;
    border: 1px solid #005c75;
    background-color: #f8f9fa;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
  }
`;

export default StyledTooltip;
