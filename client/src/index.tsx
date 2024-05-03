import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import GmailRedirect from './oauth-redirect/GmailRedirect';

<>
  <script src="particle-image.js"/>
  <script src="particle-image.min.js"/>
  <script src="http://localhost:8888/eel.js"/>
</>
const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/gmail/auth" element={<GmailRedirect/>} />
        <Route path="/" element={<App/>} />
      </Routes>
    </BrowserRouter>
    {/* <App/> */}
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
