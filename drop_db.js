// A graph traversal example for Arango DB.
// USAGE: $ npm install
//        $ node traverse_example.js
//
// 1) It will create "ingenium_db_test" db if it does not exist. Then it creates a graph, add verticies and edges.
// A traverse query is made to get hierarchical json structure of an "execution".
// 2) If "ingenium_db_test" db exists, it will be dropped. This is done to reset the database for the next run.

var { Database } = require('arangojs');
var db = new Database({ url: 'http://localhost:8529', auth: { username: 'root', password: 'somepassword' } });
var database_name = 'ingenium';
console.log('Run script');
db.listDatabases()
.then((names)=> {
    if (names.indexOf(database_name) > -1) {
      db.dropDatabase(database_name);
      console.log('Database dropped:', database_name);
    } else {
      console.log('Database not found:', database_name);
    }
  }, (err) => {
    console.error('Failed to get list of databases');
});
