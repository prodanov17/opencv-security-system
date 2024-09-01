import { SettingsIcon } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

const API_URL = import.meta.env.VITE_API_URL;

interface Camera {
  id: number;
  name: string;
  armed: boolean;
}

function FeedSelection() {
  //fetch cameras
  const [cameras, setCameras] = useState<Camera[]>([]);
  const [error, setError] = useState<string | null>(null);

  const fetchCameras = async () => {
    try {
      const response = await fetch(`${API_URL}/cameras`);
      const data = await response.json();
      if (response.ok) {
        setCameras(data.cameras);
        setError(null);
      } else {
        setError(data.error);
      }
    } catch (error) {
      setError("Failed to fetch cameras");
    }
  };

  useEffect(() => {
    fetchCameras();
  }, []);
  return (
    <div className="mt-20 p-8 flex flex-col gap-4">
      <h1 className="font-semibold text-xl">Feed Selection</h1>
      <div className="space-y-4">
        {error && <p className="text-red-500">{error}</p>}
        {cameras &&
          cameras.map((camera) => (
            <div
              key={camera.id}
              className="bg-white shadow-md rounded-lg p-6 flex justify-between items-center"
            >
              <div>
                <h3
                  className={`text-xs uppercase ${camera.armed ? "text-green-400" : "text-red-400"}`}
                >
                  {camera.armed ? "armed" : "disarmed"}
                </h3>
                <h2 className="text-lg font-medium">{camera.name}</h2>
                <Link
                  to={`/feed/${camera.id}`}
                  className="text-blue-500 hover:underline"
                >
                  View Live Feed
                </Link>
              </div>
              <Link to={`/settings/${camera.id}`}>
                <SettingsIcon />
              </Link>
            </div>
          ))}
      </div>
      <Link to="/feed/new" className="text-blue-500 hover:underline">
        Add Camera
      </Link>
    </div>
  );
}

export default FeedSelection;
