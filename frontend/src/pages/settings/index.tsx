import { SwitchDemo } from "@/ui/shad/Switch";
import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

const algorithms = [
  { name: "Machine Learning", val: "ml" },
  { name: "Histogram of Gradients", val: "hog" },
  { name: "Background Subtraction", val: "mog" },
];
const API_URL = import.meta.env.VITE_API_URL;

function Settings() {
  const { id } = useParams(); // Get camera ID from URL parameters
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [algorithm, setAlgorithm] = useState(algorithms[0]);
  const [notificationsEnabled, setNotificationsEnabled] = useState(false);
  const [armed, setArmed] = useState(false);
  const [showSource, setShowSource] = useState(false);
  const [source, setSource] = useState("");

  useEffect(() => {
    const fetchCameraData = async () => {
      try {
        const response = await fetch(`${API_URL}/cameras/${id}`);
        if (response.ok) {
          const data = await response.json();
          setName(data.name);
          setAlgorithm(data.algorithm);
          setNotificationsEnabled(data.notifications_enabled);
          setArmed(data.armed);
          setSource(data.source);
        } else {
          alert("Failed to fetch camera data");
        }
      } catch (error) {
        console.error("Error fetching camera data:", error);
        alert("An error occurred while fetching camera data");
      }
    };

    fetchCameraData();
  }, [id]);

  const handleDelete = () => async () => {
    try {
      const response = await fetch(`${API_URL}/cameras/${id}`, {
        method: "DELETE",
      });

      if (response.ok) {
        alert("Camera deleted successfully");
        navigate("/feed"); // Redirect to the cameras list or another relevant page
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.message}`);
      }
    } catch (error) {
      console.error("Error deleting camera:", error);
      alert("An error occurred while deleting the camera");
    }
  }

  const handleSave = async () => {
    try {
      let reqBody = {
        name: name,
        algorithm: algorithm,
        notifications_enabled: notificationsEnabled,
      };

      if (showSource) {
        reqBody = { ...reqBody, source: source };
      }

      const response = await fetch(`${API_URL}/cameras/${id}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(reqBody),
      });

      if (response.ok) {
        alert("Settings updated successfully");
        navigate("/feed"); // Redirect to the cameras list or another relevant page
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.message}`);
      }
    } catch (error) {
      console.error("Error updating camera settings:", error);
      alert("An error occurred while updating settings");
    }
  };

  return (
    <div className="p-8 bg-white shadow-md rounded-lg mt-16">
      <h2 className="text-2xl font-semibold mb-4">Camera Settings</h2>
      <div className="mb-4">
        <label
          htmlFor="name"
          className="block text-sm font-medium text-gray-700"
        >
          Camera Name
        </label>
        <input
          type="text"
          id="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        />
      </div>
      <div className="mb-4">
        <label
          htmlFor="algorithm"
          className="block text-sm font-medium text-gray-700"
        >
          Algorithm
        </label>
        <select
          id="algorithm"
          value={algorithm}
          onChange={(e) => setAlgorithm(e.target.value)}
          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        >
          {algorithms.map((algo) => (
            <option key={algo} value={algo.val}>
              {algo.name}
            </option>
          ))}
        </select>
      </div>
      <div className="mb-4 flex items-center justify-between">
        <label
          htmlFor="notifications"
          className="block text-sm font-medium text-gray-700"
        >
          Notifications Enabled
        </label>
        <SwitchDemo
          armed={notificationsEnabled}
          label=""
          callback={setNotificationsEnabled}
        />
      </div>
      <div className="mb-4 flex items-center gap-2 mt-4">
        <input
          type="checkbox"
          id="source"
          name="source"
          onChange={() => setShowSource((prev) => !prev)}
        />
        <label
          htmlFor="source"
          className="block text-sm font-medium text-gray-700"
        >
          Custom Source
        </label>
      </div>
      {showSource && (
        <div className="mb-4">
          <label
            htmlFor="source"
            className="block text-sm font-medium text-gray-700"
          >
            Camera Source
          </label>
          <input
            type="text"
            id="name"
            value={source}
            onChange={(e) => setSource(e.target.value)}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          />
        </div>
      )}

      <button
        onClick={handleSave}
        className="w-full bg-indigo-600 text-white px-4 py-2 rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
      >
        Save Settings
      </button>
      <button
        onClick={handleDelete}
        className="w-full bg-red-600 text-white px-4 py-2 rounded-md shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 mt-4"
      >
        Delete Camera
      </button>
    </div>
  );
}

export default Settings;
// <div className="mb-4 flex items-center justify-between">
// <label
// htmlFor="armed"
// className="block text-sm font-medium text-gray-700"
// >
// Armed
// </label>
// <SwitchDemo
// label="Armed"
// armed={armed}
// callback={setArmed}
// />
// </div>
