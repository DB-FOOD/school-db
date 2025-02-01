const express = require("express");
const cors = require("cors");
const serverless = require("serverless-http");
const { Pool } = require("pg");
require("dotenv").config();

const app = express();

app.use(express.json());
app.use(cors());

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

const connectToDB = async () => {
  try {
    const connection = await pool.connect();
    console.log("connection successful");
    connection.release();
  } catch (err) {
    console.error("something went wrong", err);
  }
};

connectToDB();

// Routes
app.get("/", (req, res) => {
  res.send("Server is running!");
});

app.get("/customers", async (req, res) => {
  try {
    const result = await pool.query("SELECT * FROM customers");
    res.json(result.rows);
  } catch (err) {
    console.error("Error fetching customers:", err);
    res.status(500).send("Internal Server Error");
  }
});

app.post("/customers", async (req, res) => {
  const { name, address, city, country } = req.body;
  if (!name || !address || !city || !country) {
    return res.status(400).send("All fields are required");
  }

  try {
    const result = await pool.query(
      "INSERT INTO customers (name, address, city, country) VALUES ($1, $2, $3, $4) RETURNING *",
      [name, address, city, country]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    console.error("Error adding customer:", err);
    res.status(500).send("Internal Server Error");
  }
});

// Serverless export
module.exports = app;
module.exports.handler = serverless(app);
