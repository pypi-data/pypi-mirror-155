import { AnyObject } from 'tsdef';
import Ajv, { ErrorObject } from 'ajv';
import {
  WorkflowSchema,
  ParameterSection,
  ParameterSectionProps
} from './types';

export function validateSchema(data: AnyObject, schema: AnyObject): any {
  // Slower, todo: manage workflow schemas
  // and use ajv singleton
  const ajv = new Ajv({
    allErrors: true,
    strictSchema: false,
    verbose: true
  });
  const validate = ajv.compile(schema);
  const valid = validate(data);
  return { valid, errors: validate.errors };
}

export const groupErrorsByParam = (
  errors: ErrorObject[]
): { [key: string]: string[] } => {
  const errorMapping: { [key: string]: string[] } = {};
  errors.forEach(Error => {
    Object.values(Error.params as AnyObject).forEach(key => {
      errorMapping[key] = [...(errorMapping[key] || []), Error.message || ''];
    });
  });
  return errorMapping;
};

export const excludeHiddenParameters = (
  parameters: ParameterSectionProps
): ParameterSectionProps =>
  Object.fromEntries(
    Object.entries(parameters).filter(([_, Property]) => !Property.hidden)
  );

export const excludeNamedParameters = (
  parameters: ParameterSectionProps,
  names: string[]
): ParameterSectionProps =>
  Object.fromEntries(
    Object.entries(parameters).filter(([key, _]) => !names.includes(key))
  );

export const getSchemaSections = (
  schema: WorkflowSchema,
  filterHidden = true,
  filterNames: string[] = ['out_dir']
): ParameterSection[] => {
  return Object.values(schema.definitions)
    .map(Section => ({
      ...Section,
      properties: excludeNamedParameters(
        filterHidden
          ? excludeHiddenParameters(Section.properties)
          : Section.properties,
        filterNames
      )
    }))
    .filter(Def => Object.keys(Def.properties).length !== 0);
};
