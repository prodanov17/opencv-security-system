import { Route, Routes } from "react-router-dom"
import Home from "./pages/home"
import Navbar from "./components/Navbar"
import Feed from "./pages/feed"
import Logs from "./pages/logs"
import FeedSelection from "./pages/feed/FeedSelection"
import Settings from "./pages/settings"
import AddCamera from "./pages/feed/AddCamera"

function App() {

  return (
    <>
    <Navbar/>
    <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/feed" element={<FeedSelection />} />
        <Route path="/feed/new" element={<AddCamera />} />
        <Route path="/feed/:id" element={<Feed />} />
        <Route path="/settings/:id" element={<Settings />} />
        <Route path="/logs" element={<Logs />} />
    </Routes>
    </>
  )
}

export default App
