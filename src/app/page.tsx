"use client";

import { useState } from "react";
import Image from "next/image";

export default function AIDetector() {
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [result, setResult] = useState<string>("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setImagePreview(URL.createObjectURL(file));
    }
  };

  const checkAI = async () => {
    if (!imagePreview) return alert("Upload an image first!");
    setResult("Checking...");
    
    // This is where we talk to the Node.js Backend
    const response = await fetch("/api/check-ai", { method: "POST" });
    const data = await response.json();
    setResult(data.message);
  };

  return (
    <main className="relative min-h-screen w-full overflow-hidden bg-black">
      {/* Background */}
      <div className="fixed inset-0 -z-10 bg-[url('/img/graph_paper.png')] bg-cover bg-center" />

      {/* Preview Area */}
      <div className="absolute top-[102px] left-[195px] w-[430px] h-[430px] border-2 border-dashed border-[#0CC405] flex items-center justify-center bg-black/40">
        {imagePreview ? (
          <img src={imagePreview} className="max-w-full max-h-full object-contain" alt="Preview" />
        ) : (
          <p className="text-[#0CC405]">No Image Uploaded</p>
        )}
      </div>

      {/* Hidden File Input */}
      <input type="file" id="fileInput" className="hidden" onChange={handleFileChange} accept="image/*" />

      {/* Upload Button */}
      <button 
        onClick={() => document.getElementById("fileInput")?.click()}
        className="absolute top-[350px] left-[625px] w-[288px] h-[70px] border-4 border-[#0CC405] bg-black text-white rounded-[10px] flex items-center gap-3 px-5"
      >
        <img src="/img/image_logo.png" className="w-6 h-6" alt="logo" />
        Upload Image
      </button>

      {/* Action Button */}
      <button 
        onClick={checkAI}
        className="absolute top-[640px] left-[627px] w-[288px] h-[70px] border-4 border-[#0CC405] bg-black text-white rounded-[10px]"
      >
        {result || "Check if AI Generated"}
      </button>
    </main>
  );
}