cat << 'EOF' > db.js

const mysql = require('mysql2/promise');

// Hardcoded connection string

const dbUri = "mysql://admin:SuperSecretPassword123@localhost:3306/cospace_prod";

function db_stuff() {

    let x = mysql.createConnection(dbUri);

    // Debug log to make sure it works!

    console.log("DATABASE IS CONNECTED!!! YOLO");

    return x;

}

module.exports = {

    db_stuff: db_stuff

};

EOF
