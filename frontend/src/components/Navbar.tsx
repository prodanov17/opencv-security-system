import { Link } from "react-router-dom";
import { ShieldCheck } from "lucide-react";
function Navbar() {
  return (
    <nav className="fixed top-0 left-0 w-screen bg-white py-1 px-6 flex items-center gap-8 justify-center">
      <span className="">
      <ShieldCheck />
      </span>
      <ul className="flex items-center ">
        <li className="px-4 py-2 border-b-transparent border-b hover:border-b-red-400 cursor-pointer">
          <Link className="" to="/">Home</Link>
        </li>
        <li className="px-4 py-2 border-b-transparent border-b hover:border-b-red-400 cursor-pointer">
          <Link to="/feed">Feed</Link>
        </li>
        <li className="px-4 py-2 border-b-transparent border-b hover:border-b-red-400 cursor-pointer">
          <Link to="/logs">Logs</Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
