'use strict';

// The env variable is like artifactory.jpl.nasa.gov:16003/gov/nasa/jpl/ingenium/core_server:r13_1_1
module.exports.version = process.env.ARCHIVE_ING_IMAGE ? process.env.ARCHIVE_ING_IMAGE.split(':').pop().split('_').join('.') : '';
module.exports.api_version = 'v5';
module.exports.database_name = 'ingenium';
module.exports.db_url = process.env.ARANGODBURL ? process.env.ARANGODBURL : 'http://localhost:8529';
module.exports.db_password = process.env.ARANGO_ROOT_PASSWORD ? process.env.ARANGO_ROOT_PASSWORD : 'somepassword';
module.exports.db_user = process.env.ARANGO_USER ? process.env.ARANGO_USER : 'root';
module.exports.execution_id_prefix = process.env.EXECUTION_ID_PREFIX ? process.env.EXECUTION_ID_PREFIX : 'clipper-ingenium-';
module.exports.procedure_id_prefix = process.env.PROCEDURE_ID_PREFIX ? process.env.PROCEDURE_ID_PREFIX : 'clipper-procedure-';
module.exports.public_pem = process.env.PUBLIC_PEM || '';

