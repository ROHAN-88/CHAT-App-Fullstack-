import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import Login from "./Login";
import "bootstrap/dist/css/bootstrap.min.css";
const App = () => {
  return (
    <Router>
      <Routes>
        {/* <Route path="/" element={<Register />} /> */}
        <Route path="/login" element={<Login />} />
        {/* <Routeo
          path="/chat"
          element={user ? <Chat user={user} /> : <Login setUser={setUser} />}
        /> */}
        {/* <Route
          path="/messages"
          element={
            user ? <MessageList user={user} /> : <Login setUser={setUser} />
          }
        /> */}
      </Routes>
    </Router>
  );
};

export default App;
