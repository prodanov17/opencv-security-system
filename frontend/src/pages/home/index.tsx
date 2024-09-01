import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="h-screen flex flex-col items-center justify-center bg-gray-100">
      <div className="text-center p-8 bg-white shadow-lg rounded-lg max-w-lg">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Welcome to Our App!</h1>
        <p className="text-lg text-gray-700 mb-6">Explore and manage your cameras with ease. Start by navigating to your feeds or logs.</p>
        <div className="flex gap-4 justify-center">
          <Link 
            to="/feeds" 
            className="bg-blue-500 text-white py-2 px-4 rounded-lg shadow hover:bg-blue-600 transition duration-300"
          >
            View Feeds
          </Link>
          <Link 
            to="/logs" 
            className="bg-green-500 text-white py-2 px-4 rounded-lg shadow hover:bg-green-600 transition duration-300"
          >
            Logs
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Home;

