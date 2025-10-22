# 🚀 Testing Your Blockchain with Postman

This guide shows how to test the provided Python Blockchain using **Postman** to send HTTP requests to the **Flask** API.

---

## 🧠 Prerequisites

Make sure you have installed:

- **Python 3**
- **Postman**
- **Flask** (install with pip):

```bash
pip install flask
```

---

## ⚙️ 1. Run the Flask server

Save your blockchain code to a file, for example:

```bash
blockchain.py
```

Run the server:

```bash
python blockchain.py
```

You should see something like:

```
 * Running on http://0.0.0.0:5000/
```

The API will be listening on port **5000**.

---

## 🌐 2. Configure Postman

Open **Postman** and (optionally) create a new **Collection** named `Blockchain API`.

Add the following requests:

### 🧩 2.1. `GET /mine_block`

- **Method:** `GET`
- **URL:** `http://127.0.0.1:5000/mine_block`

**What it does:** Mines (creates) a new block and appends it to the chain.

**Expected response example:**

```json
{
  "message": "Congratulations, you’ve mined a block",
  "index": 2,
  "timestamp": "2025-10-22 11:32:47.123456",
  "proof": 533,
  "previous_hash": "00abf9c..."
}
```

---

### 📜 2.2. `GET /get_chain`

- **Method:** `GET`
- **URL:** `http://127.0.0.1:5000/get_chain`

**What it does:** Returns the full blockchain.

**Expected response example:**

```json
{
  "chain": [
    {
      "index": 1,
      "timestamp": "2025-10-22 11:30:00.000000",
      "proof": 1,
      "previous_hash": "0"
    },
    {
      "index": 2,
      "timestamp": "2025-10-22 11:32:47.123456",
      "proof": 533,
      "previous_hash": "00abf9c..."
    }
  ],
  "length": 2
}
```

---

### ✅ 2.3. `GET /is_valid`

- **Method:** `GET`
- **URL:** `http://127.0.0.1:5000/is_valid`

**What it does:** Verifies whether the current blockchain is valid.

**Expected response example:**

```json
{
  "is_valid": true
}
```

---

## 🧪 3. Testing tips

- After each `/mine_block` request, call `/get_chain` to inspect the newly added block(s).
- Modify a block in memory (or change the code to tamper with a block) and call `/is_valid` to see the validation fail (great for demonstrating immutability).
- If you want to test from another machine on the same network, run the server with `host='0.0.0.0'` (already set in the script) and use the host machine's LAN IP in Postman, e.g. `http://192.168.1.100:5000/mine_block`.
- Use Postman's **Pretty** / **Raw** views to inspect responses and compare hashes and proofs.

---

## 🔧 4. Optional enhancements to try

- Add a `/add_transaction` endpoint and a `/mine_block` modification that includes pending transactions.
- Persist the chain to disk (JSON file) so it survives server restarts.
- Expose a simple UI (HTML + fetch) to call the endpoints from a browser.

---

## 🏁 Conclusion

You now have a ready-to-use guide to test the minimal Blockchain with Postman. This is a clean, hands-on way to explore **Proof of Work**, block integrity, and how a chain detects tampering.
