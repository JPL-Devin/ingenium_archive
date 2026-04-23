'use strict';

// Mock arangojs before requiring base_funcs
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

const base_funcs = require('../../api/base_funcs');

describe('base_funcs', () => {
  describe('sanitize_internal_attrs', () => {
    it('should remove _id, _key, _rev from an object', () => {
      const obj = { _id: 'test/123', _key: '123', _rev: 'abc', name: 'test', value: 42 };
      const result = base_funcs.sanitize_internal_attrs(obj);
      expect(result).not.toHaveProperty('_id');
      expect(result).not.toHaveProperty('_key');
      expect(result).not.toHaveProperty('_rev');
      expect(result.name).toBe('test');
      expect(result.value).toBe(42);
    });

    it('should return the same object reference (mutates in place)', () => {
      const obj = { _id: 'x', _key: 'y', _rev: 'z' };
      const result = base_funcs.sanitize_internal_attrs(obj);
      expect(result).toBe(obj);
    });

    it('should handle objects that do not have internal attrs', () => {
      const obj = { name: 'hello' };
      const result = base_funcs.sanitize_internal_attrs(obj);
      expect(result.name).toBe('hello');
    });
  });

  describe('sanitize_internal_attrs_recursive', () => {
    it('should remove internal attrs from nested children', () => {
      const obj = {
        _id: 'top', _key: 'k1', _rev: 'r1', name: 'parent',
        children: [
          { _id: 'c1', _key: 'ck1', _rev: 'cr1', name: 'child1' },
          { _id: 'c2', _key: 'ck2', _rev: 'cr2', name: 'child2' },
        ],
      };
      const result = base_funcs.sanitize_internal_attrs_recursive(obj);
      expect(result).not.toHaveProperty('_id');
      expect(result.children[0]).not.toHaveProperty('_id');
      expect(result.children[1]).not.toHaveProperty('_key');
      expect(result.children[0].name).toBe('child1');
    });

    it('should remove internal attrs from run_records', () => {
      const obj = {
        _id: 'top', _key: 'k1', _rev: 'r1',
        run_records: [
          { _id: 'rr1', _key: 'rrk1', _rev: 'rrr1', data: 'record1' },
        ],
      };
      const result = base_funcs.sanitize_internal_attrs_recursive(obj);
      expect(result.run_records[0]).not.toHaveProperty('_id');
      expect(result.run_records[0].data).toBe('record1');
    });

    it('should handle objects without children or run_records', () => {
      const obj = { _id: 'a', _key: 'b', _rev: 'c', name: 'leaf' };
      const result = base_funcs.sanitize_internal_attrs_recursive(obj);
      expect(result.name).toBe('leaf');
      expect(result).not.toHaveProperty('_id');
    });
  });

  describe('sanitizeElement', () => {
    it('should delete idx from element', () => {
      const elem = { idx: 3, name: 'step1' };
      const result = base_funcs.sanitizeElement(elem);
      expect(result).not.toHaveProperty('idx');
      expect(result.name).toBe('step1');
    });

    it('should convert parent_idd to parent_id for execution prefix', () => {
      const elem = { parent_idd: 'execution/abc123' };
      const result = base_funcs.sanitizeElement(elem);
      expect(result.parent_id).toBe('');
      expect(result).not.toHaveProperty('parent_idd');
    });

    it('should convert parent_idd to parent_id for procedureVersion prefix', () => {
      const elem = { parent_idd: 'procedureVersion/xyz789' };
      const result = base_funcs.sanitizeElement(elem);
      expect(result.parent_id).toBe('');
    });

    it('should extract parent_id from parent_idd for element prefix', () => {
      const elem = { parent_idd: 'element/parent-id-123' };
      const result = base_funcs.sanitizeElement(elem);
      expect(result.parent_id).toBe('parent-id-123');
    });

    it('should delete _version', () => {
      const elem = { _version: 5 };
      const result = base_funcs.sanitizeElement(elem);
      expect(result).not.toHaveProperty('_version');
    });

    it('should recurse into children', () => {
      const elem = {
        idx: 0,
        children: [
          { idx: 1, parent_idd: 'element/child1', _version: 2 },
        ],
      };
      const result = base_funcs.sanitizeElement(elem);
      expect(result.children[0]).not.toHaveProperty('idx');
      expect(result.children[0]).not.toHaveProperty('_version');
      expect(result.children[0].parent_id).toBe('child1');
    });

    it('should handle run_records by deleting nested run_records', () => {
      const elem = {
        run_records: [
          { idx: 0, run_records: [{ nested: true }], parent_idd: 'element/rr1' },
        ],
      };
      const result = base_funcs.sanitizeElement(elem);
      expect(result.run_records[0]).not.toHaveProperty('run_records');
      expect(result.run_records[0]).not.toHaveProperty('idx');
    });
  });

  describe('push_error', () => {
    it('should wrap string errors with message and details', () => {
      const result = base_funcs.push_error('Something failed', 'detailed reason');
      expect(result.message).toBe('Something failed');
      expect(result.details).toContain('detailed reason');
    });

    it('should handle object errors with message property', () => {
      const err = { message: 'original error', code: 500 };
      const result = base_funcs.push_error('Wrapped error', err);
      expect(result.message).toBe('Wrapped error');
      expect(result.details).toEqual(expect.arrayContaining(['original error']));
    });

    it('should handle errors that cannot be JSON.stringified', () => {
      const circular = {};
      circular.self = circular;
      const result = base_funcs.push_error('Circular error', circular);
      expect(result.message).toBe('Circular error');
      expect(result.details).toBeDefined();
      expect(result.details.length).toBeGreaterThan(0);
    });

    it('should create details array if not present on error', () => {
      const err = { code: 404 };
      const result = base_funcs.push_error('Not found', err);
      expect(result.message).toBe('Not found');
      expect(Array.isArray(result.details)).toBe(true);
    });
  });

  describe('remove_execution_time_input_fields', () => {
    it('should remove fields not in authoring_user_input spec', () => {
      const elem = {
        authoring_user_input: { field1: 'val1', extra_field: 'val2' },
        specification: {
          authoring_user_input: { field1: 'spec1' },
        },
      };
      base_funcs.remove_execution_time_input_fields(elem);
      expect(elem.authoring_user_input.field1).toBe('val1');
      expect(elem.authoring_user_input).not.toHaveProperty('extra_field');
    });

    it('should handle nested objects', () => {
      const elem = {
        authoring_user_input: {
          nested: { keep: 'yes', remove: 'no' },
        },
        specification: {
          authoring_user_input: {
            nested: { keep: 'spec' },
          },
        },
      };
      base_funcs.remove_execution_time_input_fields(elem);
      expect(elem.authoring_user_input.nested.keep).toBe('yes');
      expect(elem.authoring_user_input.nested).not.toHaveProperty('remove');
    });

    it('should handle entries array', () => {
      const elem = {
        authoring_user_input: {
          entries: [{ keep_field: 'yes', extra: 'no' }],
        },
        specification: {
          authoring_user_input: {
            entries: [{ keep_field: 'spec' }],
          },
        },
      };
      base_funcs.remove_execution_time_input_fields(elem);
      expect(elem.authoring_user_input.entries[0].keep_field).toBe('yes');
      expect(elem.authoring_user_input.entries[0]).not.toHaveProperty('extra');
    });

    it('should do nothing if specification does not have authoring_user_input', () => {
      const elem = {
        authoring_user_input: { field1: 'val1' },
        specification: {},
      };
      base_funcs.remove_execution_time_input_fields(elem);
      expect(elem.authoring_user_input.field1).toBe('val1');
    });
  });

  describe('sortChildren', () => {
    it('should sort children by idx', () => {
      const node = {
        children: [
          { idx: 2, name: 'c' },
          { idx: 0, name: 'a' },
          { idx: 1, name: 'b' },
        ],
      };
      base_funcs.sortChildren(node);
      expect(node.children[0].name).toBe('a');
      expect(node.children[1].name).toBe('b');
      expect(node.children[2].name).toBe('c');
    });

    it('should sort run_records by idx', () => {
      const node = {
        run_records: [
          { idx: 1, data: 'second' },
          { idx: 0, data: 'first' },
        ],
      };
      base_funcs.sortChildren(node);
      expect(node.run_records[0].data).toBe('first');
      expect(node.run_records[1].data).toBe('second');
    });

    it('should recursively sort nested children', () => {
      const node = {
        children: [
          {
            idx: 0, name: 'parent',
            children: [
              { idx: 1, name: 'b' },
              { idx: 0, name: 'a' },
            ],
          },
        ],
      };
      base_funcs.sortChildren(node);
      expect(node.children[0].children[0].name).toBe('a');
    });

    it('should handle node without children', () => {
      const node = { name: 'leaf' };
      expect(() => base_funcs.sortChildren(node)).not.toThrow();
    });
  });

  describe('get_sj_error_message', () => {
    it('should extract errorMessage from response body', () => {
      const err = { response: { body: { errorMessage: 'DB error' } } };
      expect(base_funcs.get_sj_error_message(err)).toBe('DB error');
    });

    it('should handle non-string errorMessage', () => {
      const err = { response: { body: { errorMessage: { complex: true } } } };
      const result = base_funcs.get_sj_error_message(err);
      expect(result).toContain('complex');
    });

    it('should return empty string if response body has no errorMessage', () => {
      const err = { response: { body: {} } };
      expect(base_funcs.get_sj_error_message(err)).toBe('');
    });

    it('should return inspected error for non-response errors', () => {
      const err = new Error('regular error');
      const result = base_funcs.get_sj_error_message(err);
      expect(result).toContain('regular error');
    });
  });

  describe('prepareElementForCopy', () => {
    beforeEach(() => {
      const uuid = require('uuid');
      uuid.v4.mockReturnValue('mock-uuid-1234');
    });

    afterEach(() => {
      const uuid = require('uuid');
      uuid.v4.mockReset();
    });

    it('should assign new elem_id and _key', () => {
      const elem = {
        elem_id: 'old-id',
        _key: 'old-key',
        _id: 'element/old-id',
        elem_type: 'STEP',
        parent_idd: 'execution/root',
        idx: 0,
        tag_ids: [],
        break_point: 'SOME',
      };
      const elems_to_add = [];
      const edges_to_add = [];
      base_funcs.prepareElementForCopy('EXECUTION', 'PROCEDURE', elem, [], elems_to_add, edges_to_add);
      expect(elem.elem_id).toBe('mock-uuid-1234');
      expect(elem._key).toBe('mock-uuid-1234');
      expect(elem).not.toHaveProperty('_id');
      expect(elem.conversations).toEqual([]);
      expect(elem.break_point).toBe('NONE');
      expect(elems_to_add.length).toBe(1);
      expect(edges_to_add.length).toBe(1);
    });

    it('should use procedureElement prefix for PROCEDURE target', () => {
      const elem = {
        elem_id: 'old-id',
        _key: 'old-key',
        elem_type: 'SECTION',
        parent_idd: 'procedureVersion/root',
        idx: 0,
        tag_ids: [],
      };
      const edges = [];
      base_funcs.prepareElementForCopy('PROCEDURE', 'PROCEDURE', elem, [], [], edges);
      expect(edges[0]._to).toContain('procedureElement/');
    });

    it('should use element prefix for EXECUTION target', () => {
      const elem = {
        elem_id: 'old-id',
        _key: 'old-key',
        elem_type: 'SECTION',
        parent_idd: 'execution/root',
        idx: 0,
        tag_ids: [],
      };
      const edges = [];
      base_funcs.prepareElementForCopy('EXECUTION', 'EXECUTION', elem, [], [], edges);
      expect(edges[0]._to).toContain('element/');
    });
  });

  describe('execution_meta_data_template', () => {
    it('should have expected structure', () => {
      const template = base_funcs.execution_meta_data_template;
      expect(template.test_conductor).toBe('');
      expect(template.time_started).toBe('');
      expect(template.time_completed).toBe('');
      expect(template.status).toBe('NONE');
      expect(template.error).toEqual({});
    });
  });
});
