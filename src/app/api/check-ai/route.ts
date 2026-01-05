import { NextResponse } from "next/server";

export async function POST() {
  // This is pure Node.js environment
  // In the future, you will put your AI detection logic here
  
  // For now, we simulate a delay and return a fake result
  await new Promise((resolve) => setTimeout(resolve, 2000));

  return NextResponse.json({ 
    message: "Result: 85% Likely AI Generated" 
  });
}