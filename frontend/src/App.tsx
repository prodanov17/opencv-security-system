import { Route, Routes } from "react-router-dom"
import Home from "./pages/home"
import Navbar from "./components/Navbar"
import Feed from "./pages/feed"
import Logs from "./pages/logs"

function App() {

  return (
    <>
    <Navbar/>
    <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/feed" element={<Feed />} />
        <Route path="/logs" element={<Logs />} />
    </Routes>
    </>
  )
}

export default App
