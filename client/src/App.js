import InputTodo from "./components/InputTodo";
import ListTodos from "./components/ListTodos";
import { useState, useEffect } from "react";

// const fetch = require('node-fetch')

// async function fetchData() {

//   try {
//     const response = await fetch("http://localhost:8001")
//     const body = await response.text();
//     console.log(body)
//   }
//   catch (error) {
//     console.error("Error fetching data:", error)
//   }

// }

// fetchData()



// import './App.css';
import './styles.css';

function App() {
  const [response1, setResponse1] = useState('Please instert your data');
  const [response2, setResponse2] = useState('Please instert your data');
  const [chatresponse1, chatsetResponse1] = useState('Please instert your data');
  const [chatresponse2, chatsetResponse2] = useState('Please instert your data');


  const handleAll = async (event) => {
    // Ensure sequential execution of all handlers
    handleUnchanged(event);
    await handleInputChange(event);
    await handleBiasedChat(event);
    await handleUnbiasedChat(event);
  }

  const handleUnchanged = async (event) => {
    const userInput = event.target.value;
    try {
      setResponse1(userInput);
    } catch (error) {
      console.error('Error:', error);
    }
  };
  const handleInputChange = async (event) => {
    // Get the user input from the event
    const userInput = event.target.value;
    try {
      console.log("Sending request to /chatquery");

      // Make a GET request to the FastAPI /chatquery endpoint
      const fetchResponse = await fetch(`http://localhost:8000/chatquery?sentence=${encodeURIComponent(userInput)}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      // Parse the response from the server
      const data = await fetchResponse.json();

      if (data.filteredSentence !== undefined) {
        // Update the response state with the filtered sentence
        setResponse2(data.filteredSentence);
      } else {
        console.error('Invalid server response:', data);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleUnbiasedChat = async (event) => {
    const userInput = event.target.value;
    try {
      console.log("Sending request to /query_chat_response");

      const fetchResponse = await fetch(`http://localhost:8000/query_chat_response?sentence=${encodeURIComponent(userInput)}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const data = await fetchResponse.json();

      if (data.openai_response !== undefined) {
        chatsetResponse2(data.openai_response); // Update with unbiased response
      } else {
        console.error('Invalid server response:', data);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleBiasedChat = async (event) => {
    const userInput = event.target.value;
    try {
      console.log("Sending request to /query_openai_direct");

      const fetchResponse = await fetch(`http://localhost:8000/query_openai_direct?input_str=${encodeURIComponent(userInput)}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const data = await fetchResponse.json();

      if (data.openai_response !== undefined) {
        chatsetResponse1(data.openai_response); // Update with biased response
      } else {
        console.error('Invalid server response:', data);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };




  return (
    <div className="container">
      <header>
        <h1>Real Time X-tract</h1>
        <p>Dissolving word bias for better trained AI systems</p>
      </header>
      <main>
        <section className="welcome">
          <h4>Please insert your paragraph below to see the impact of the Word bias on an AI System </h4>
        </section>
        <hr /> {/* Horizontal line to divide sections */}
        <section className="user-section">
          <div className="container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            <div style={{ textAlign: 'center', maxWidth: '600px', width: '100%' }}>
              <input
                type="text"
                id="userQuestion"
                placeholder="Type your question..."
                style={{
                  width: '100%',
                  padding: '15px',
                  fontSize: '18px',
                  borderRadius: '5px',
                  border: '1px solid #ccc',
                  outline: 'none',
                  marginBottom: '20px'
                }}
              />
              <button
                onClick={() => handleAll({ target: { value: document.getElementById("userQuestion").value } })}
                style={{
                  width: '100%',
                  padding: '15px',
                  fontSize: '18px',
                  backgroundColor: '#4CAF50',
                  color: 'white',
                  border: 'none',
                  borderRadius: '5px',
                  cursor: 'pointer'
                }}
              >
                Submit
              </button>
            </div>
          </div>
        </section>
        <hr /> {/* Horizontal line to divide sections */}
        <section className="currency-rates" style={{ display: 'flex', justifyContent: 'space-between', gap: '20px' }}>
          <div className="chatbot" style={{ flex: 1 }}>
            <h2>Unchanged Dataset</h2>
            <div className="chat-response" style={{ minHeight: '150px', width: '100%', border: '1px solid #ccc', padding: '10px' }}>
              {response1}
            </div>
          </div>
          <div className="chatbot" style={{ flex: 1 }}>
            <h2>Dataset with removed bias</h2>
            <div className="chat-response" style={{ minHeight: '150px', width: '100%', border: '1px solid #ccc', padding: '10px' }}>
              {response2}
            </div>
          </div>
        </section>
        <section className="currency-rates" style={{ display: 'flex', justifyContent: 'space-between', gap: '20px' }}>
          <div className="chatbot" style={{ flex: 1 }}>
            <h2>AI summary from unchanged dataset</h2>
            <div className="chat-response" style={{ minHeight: '300px', width: '100%', border: '1px solid #ccc', padding: '10px' }}>
              {chatresponse1}
            </div>
          </div>
          <div className="chatbot" style={{ flex: 1 }}>
            <h2>AI summary from dataset with removed bias</h2>
            <div className="chat-response" style={{ minHeight: '300px', width: '100%', border: '1px solid #ccc', padding: '10px' }}>
              {chatresponse2}
            </div>
          </div>
        </section>

        <section className="cta">

        </section>
      </main>
      <footer>
        <p>&copy; 2024 Real Time X-tract. All rights reserved.</p>
      </footer>
    </div>
  );

}


export default App;
