'use strict';

const definitions = require('../../definitions');

describe('definitions', () => {
  describe('execution collections', () => {
    it('should export correct collection names', () => {
      expect(definitions.VENUE_GROUP).toBe('venueGroup');
      expect(definitions.VENUE).toBe('venue');
      expect(definitions.NEXT_RUN).toBe('nextRun');
      expect(definitions.ELEMENT).toBe('element');
      expect(definitions.STEP_ORDER).toBe('stepOrder');
      expect(definitions.REVISION).toBe('revision');
      expect(definitions.EXECUTION).toBe('execution');
      expect(definitions.EXECUTION_ID_GEN).toBe('execution_id_gen');
      expect(definitions.RUN_RECORD).toBe('runRecord');
    });
  });

  describe('execution graphs', () => {
    it('should export correct graph names', () => {
      expect(definitions.EXECUTION_GRAPH).toBe('execution_graph');
      expect(definitions.HISTORY_GRAPH).toBe('history_graph');
    });
  });

  describe('procedure collections', () => {
    it('should export correct procedure collection names', () => {
      expect(definitions.PROCEDURE).toBe('procedure');
      expect(definitions.PROCEDURE_ELEMENT).toBe('procedureElement');
      expect(definitions.PROCEDURE_STEP_ORDER).toBe('procedureStepOrder');
      expect(definitions.PROCEDURE_VERSION).toBe('procedureVersion');
      expect(definitions.HAS_VERSION).toBe('hasVersion');
      expect(definitions.PROCEDURE_ID_GEN).toBe('procedure_id_gen');
      expect(definitions.PROCEDURE_LABEL).toBe('procedureLabel');
    });
  });

  describe('procedure graph', () => {
    it('should export correct procedure graph name', () => {
      expect(definitions.PROCEDURE_GRAPH).toBe('procedure_graph');
    });
  });

  describe('ProcedureModificationStatus', () => {
    it('should have all expected status values', () => {
      const pms = definitions.PMS;
      expect(pms.NONE).toBe('NONE');
      expect(pms.ORIGINAL).toBe('ORIGINAL');
      expect(pms.MODIFIED).toBe('MODIFIED');
      expect(pms.MODIFYING).toBe('MODIFYING');
      expect(pms.MODIFYING_OLD).toBe('MODIFYING_OLD');
      expect(pms.DELETED).toBe('DELETED');
      expect(pms.ADDED).toBe('ADDED');
    });

    it('should have exactly 7 status values', () => {
      expect(Object.keys(definitions.PMS)).toHaveLength(7);
    });
  });

  describe('ProcedureModificationType', () => {
    it('should have all expected type values', () => {
      const pmt = definitions.PMT;
      expect(pmt.NONE).toBe('NONE');
      expect(pmt.REDLINE).toBe('REDLINE');
      expect(pmt.BLUELINE).toBe('BLUELINE');
    });

    it('should have exactly 3 type values', () => {
      expect(Object.keys(definitions.PMT)).toHaveLength(3);
    });
  });

  describe('CommentStatus', () => {
    it('should have all expected status values', () => {
      expect(definitions.CommentStatus.UNRESOLVED).toBe('UNRESOLVED');
      expect(definitions.CommentStatus.RESOLVED).toBe('RESOLVED');
    });

    it('should have exactly 2 status values', () => {
      expect(Object.keys(definitions.CommentStatus)).toHaveLength(2);
    });
  });
});
