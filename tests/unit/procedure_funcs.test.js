'use strict';

// Mock arangojs before requiring anything
const mockCollection = {
  documents: jest.fn(),
  removeAll: jest.fn(),
  save: jest.fn(),
  update: jest.fn(),
  updateAll: jest.fn(),
};

const mockDb = {
  collection: jest.fn(() => mockCollection),
  query: jest.fn(),
  listDatabases: jest.fn(),
  createDatabase: jest.fn(),
  createCollection: jest.fn(),
  graph: jest.fn(() => ({
    exists: jest.fn().mockResolvedValue(false),
    create: jest.fn().mockResolvedValue(true),
  })),
  exists: jest.fn().mockResolvedValue(true),
};

const mockSystemDb = {
  database: jest.fn(() => mockDb),
  listDatabases: jest.fn().mockResolvedValue(['_system', 'ingenium']),
};

jest.mock('arangojs', () => ({
  Database: jest.fn(() => mockSystemDb),
  aql: jest.fn((strings, ...values) => ({ query: strings.join('?'), bindVars: values })),
}));

const procedure_funcs = require('../../api/procedure_funcs');

describe('procedure_funcs', () => {
  describe('getSelectedElementsMap', () => {
    it('should build map from selected elements with elem_type', () => {
      // Need the String.prototype.format from base_funcs (loaded via require chain)
      const reference_elements = [
        { elem_id: 'e1', elem_type: 'STEP', selected: true },
        { elem_id: 'e2', elem_type: 'SECTION', selected: true },
        { elem_id: 'e3', elem_type: 'STEP', selected: false },
      ];
      const map = procedure_funcs.getSelectedElementsMap(reference_elements);
      expect(map['procedureElement/e1']).toBeDefined();
      expect(map['procedureElement/e2']).toBeDefined();
      expect(map['procedureElement/e3']).toBeUndefined();
    });

    it('should return empty map for null input', () => {
      const map = procedure_funcs.getSelectedElementsMap(null);
      expect(Object.keys(map)).toHaveLength(0);
    });

    it('should return empty map for undefined input', () => {
      const map = procedure_funcs.getSelectedElementsMap(undefined);
      expect(Object.keys(map)).toHaveLength(0);
    });

    it('should skip elements without elem_type', () => {
      const reference_elements = [
        { elem_id: 'e1', selected: true },
      ];
      const map = procedure_funcs.getSelectedElementsMap(reference_elements);
      expect(Object.keys(map)).toHaveLength(0);
    });

    it('should skip elements without selected=true', () => {
      const reference_elements = [
        { elem_id: 'e1', elem_type: 'STEP' },
      ];
      const map = procedure_funcs.getSelectedElementsMap(reference_elements);
      expect(Object.keys(map)).toHaveLength(0);
    });
  });

  describe('createProcedureLabel', () => {
    it('should reject when name is empty', async () => {
      await expect(procedure_funcs.createProcedureLabel({ name: '' }))
        .rejects.toBe('Name was not specified for procedure label');
    });

    it('should reject when name is not provided', async () => {
      await expect(procedure_funcs.createProcedureLabel({}))
        .rejects.toBe('Name was not specified for procedure label');
    });
  });
});
