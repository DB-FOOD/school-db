const express = require("express");
const app = express();
const PORT = process.env.PORT || 3500;

const { Pool } = require("pg"); 
require("dotenv").config(); 

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

app.use(express.json());

const connectToDB = async() => {
    try {
        const connection = await pool.connect()
        console.log("connection successful")
        connection.release()
    } catch (err) {
        console.error ("something went wrong", err)
    }
}

app.get("/", (req, res) => {
  res.send("Server is running!");
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
  connectToDB();
});
