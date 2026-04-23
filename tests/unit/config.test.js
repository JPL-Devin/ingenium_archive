'use strict';

describe('config', () => {
  const originalEnv = process.env;

  beforeEach(() => {
    jest.resetModules();
    process.env = { ...originalEnv };
  });

  afterAll(() => {
    process.env = originalEnv;
  });

  describe('default values (no env vars set)', () => {
    beforeEach(() => {
      delete process.env.ARCHIVE_ING_IMAGE;
      delete process.env.ARANGODBURL;
      delete process.env.ARANGO_ROOT_PASSWORD;
      delete process.env.ARANGO_USER;
      delete process.env.EXECUTION_ID_PREFIX;
      delete process.env.PROCEDURE_ID_PREFIX;
      delete process.env.PUBLIC_PEM;
    });

    it('should return empty string for version when ARCHIVE_ING_IMAGE is not set', () => {
      const config = require('../../config');
      expect(config.version).toBe('');
    });

    it('should return correct api_version', () => {
      const config = require('../../config');
      expect(config.api_version).toBe('v5');
    });

    it('should return correct database_name', () => {
      const config = require('../../config');
      expect(config.database_name).toBe('ingenium');
    });

    it('should return default db_url', () => {
      const config = require('../../config');
      expect(config.db_url).toBe('http://localhost:8529');
    });

    it('should return default db_password', () => {
      const config = require('../../config');
      expect(config.db_password).toBe('somepassword');
    });

    it('should return default db_user', () => {
      const config = require('../../config');
      expect(config.db_user).toBe('root');
    });

    it('should return default execution_id_prefix', () => {
      const config = require('../../config');
      expect(config.execution_id_prefix).toBe('clipper-ingenium-');
    });

    it('should return default procedure_id_prefix', () => {
      const config = require('../../config');
      expect(config.procedure_id_prefix).toBe('clipper-procedure-');
    });

    it('should return empty string for public_pem', () => {
      const config = require('../../config');
      expect(config.public_pem).toBe('');
    });
  });

  describe('custom values (env vars set)', () => {
    it('should parse version from ARCHIVE_ING_IMAGE', () => {
      process.env.ARCHIVE_ING_IMAGE = 'artifactory.jpl.nasa.gov:16003/gov/nasa/jpl/ingenium/core_server:r13_1_1';
      const config = require('../../config');
      expect(config.version).toBe('r13.1.1');
    });

    it('should use custom ARANGODBURL', () => {
      process.env.ARANGODBURL = 'http://custom-host:8529';
      const config = require('../../config');
      expect(config.db_url).toBe('http://custom-host:8529');
    });

    it('should use custom ARANGO_ROOT_PASSWORD', () => {
      process.env.ARANGO_ROOT_PASSWORD = 'mysecretpassword';
      const config = require('../../config');
      expect(config.db_password).toBe('mysecretpassword');
    });

    it('should use custom ARANGO_USER', () => {
      process.env.ARANGO_USER = 'customuser';
      const config = require('../../config');
      expect(config.db_user).toBe('customuser');
    });

    it('should use custom EXECUTION_ID_PREFIX', () => {
      process.env.EXECUTION_ID_PREFIX = 'test-exec-';
      const config = require('../../config');
      expect(config.execution_id_prefix).toBe('test-exec-');
    });

    it('should use custom PROCEDURE_ID_PREFIX', () => {
      process.env.PROCEDURE_ID_PREFIX = 'test-proc-';
      const config = require('../../config');
      expect(config.procedure_id_prefix).toBe('test-proc-');
    });

    it('should use custom PUBLIC_PEM', () => {
      process.env.PUBLIC_PEM = 'test-pem-content';
      const config = require('../../config');
      expect(config.public_pem).toBe('test-pem-content');
    });
  });
});
