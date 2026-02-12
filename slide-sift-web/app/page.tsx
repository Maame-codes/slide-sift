"use client";

import React, { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
// FIXED: Changed 'lucide-material' to 'lucide-react'
import { Upload, Loader2, CheckCircle, Sparkles } from "lucide-react";
import ReactMarkdown from "react-markdown";

// 1. Add these imports at the very top of page.tsx
import { toPng } from "html-to-image";
import jsPDF from "jspdf";

export default function Home() {
  const [summary, setSummary] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  //download button and PDF generation logic
  const downloadPDF = async () => {
    const element = document.getElementById("notes-content");
    if (!element) return;

    try {
      const btn = document.activeElement as HTMLButtonElement;
      const originalText = btn.innerText;
      btn.innerText = "Generating...";

      // 1. Create a container for the clone that is "off-screen" but technically visible
      const cloneContainer = document.createElement("div");
      cloneContainer.style.position = "fixed";
      cloneContainer.style.top = "0";
      cloneContainer.style.left = "-9999px"; // Move it way to the left
      cloneContainer.style.zIndex = "-1000"; // Put it behind everything
      cloneContainer.style.width = "800px"; // Standard A4 width
      cloneContainer.style.backgroundColor = "#ffffff"; // Force white background

      // 2. Clone the content
      const clone = element.cloneNode(true) as HTMLElement;

      // 3. FORCE STYLES: This fixes the "Blank Page" and "Cut Off" issues
      clone.style.height = "auto";
      clone.style.overflow = "visible";
      clone.style.maxHeight = "none";
      clone.style.color = "#000000"; // Force text to be BLACK

      // Add the clone to the container, and the container to the body
      cloneContainer.appendChild(clone);
      document.body.appendChild(cloneContainer);

      // 4. CRITICAL: Wait 100ms for the browser to "paint" the text
      await new Promise((resolve) => setTimeout(resolve, 100));

      // 5. Snap the picture
      const dataUrl = await toPng(clone, {
        cacheBust: true,
        backgroundColor: "#ffffff", // Ensure background is white
        pixelRatio: 2, // High Quality
      });

      // 6. Clean up
      document.body.removeChild(cloneContainer);

      // 7. Create PDF
      const pdf = new jsPDF("p", "mm", "a4");
      const imgProps = pdf.getImageProperties(dataUrl);
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;

      // Logic: If it's one huge image, make a custom long page
      if (pdfHeight > 297) {
        const longPdf = new jsPDF({
          orientation: "p",
          unit: "mm",
          format: [210, pdfHeight + 20],
        });
        longPdf.addImage(dataUrl, "PNG", 0, 0, 210, pdfHeight);
        longPdf.save("simplified-notes.pdf");
      } else {
        pdf.addImage(dataUrl, "PNG", 0, 0, pdfWidth, pdfHeight);
        pdf.save("simplified-notes.pdf");
      }

      btn.innerText = originalText;
    } catch (error) {
      console.error("PDF Failed:", error);
      alert("PDF Generation Failed. Please check the console.");
      const btn = document.activeElement as HTMLButtonElement;
      btn.innerText = "Download PDF";
    }
  };

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;
    setLoading(true);
    setSummary(null);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:5000/sift", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      if (data.summary) setSummary(data.summary);
    } catch (error) {
      alert("Backend connection failed. Is app.py running?");
    } finally {
      setLoading(false);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "application/pdf": [".pdf"] },
    multiple: false,
  });

  return (
    <div className="min-h-screen bg-white bg-grid-dots font-sans text-slate-900 flex flex-col">
      {/* Navigation Bar - Pure Minimalist */}
      <nav className="flex items-center justify-between px-8 py-6 border-b border-slate-100 bg-white/80 backdrop-blur-md sticky top-0 z-50">
        <div className="flex items-center space-x-1">
          <span className="text-xl font-bold tracking-tight">Slide Sift</span>
          <span className="text-orange-600 font-bold">.</span>
        </div>
      </nav>

      <main className="flex-grow max-w-5xl mx-auto pt-24 pb-32 px-6">
        {/* Hero Section */}
        <header className="text-center mb-16">
          <div className="inline-block border border-slate-200 px-3 py-1 rounded-md text-[10px] font-bold tracking-widest uppercase mb-6 bg-white">
            Beta v1.0
          </div>
          <h1 className="text-6xl md:text-7xl font-bold tracking-tighter leading-[0.9] mb-6">
            Turn chaotic slides <br />
            into <span className="text-[#FF4D00] italic">pristine</span> notes.
          </h1>
          <p className="max-w-xl mx-auto text-slate-500 text-lg leading-relaxed">
            Upload your lecture PDFs. Our AI distills them into clean,
            summarized study guides.
          </p>
        </header>

        {/* Upload Container */}
        <div className="max-w-2xl mx-auto">
          <div
            {...getRootProps()}
            className={`relative border border-dashed rounded-xl p-16 text-center transition-all duration-300 bg-white
              ${isDragActive ? "border-orange-500 bg-orange-50" : "border-slate-300 hover:border-slate-400"}`}
          >
            <input {...getInputProps()} />
            <div className="flex flex-col items-center">
              <div className="bg-slate-50 p-4 rounded-full mb-6">
                <Upload className="h-6 w-6 text-slate-400" />
              </div>
              <p className="text-lg font-bold text-slate-800 mb-1">
                Drop your slides here
              </p>
              <p className="text-slate-400 text-sm mb-6">PDF files only</p>
              <button className="px-6 py-2 border border-slate-200 rounded-md text-sm font-bold hover:bg-slate-50 transition-colors">
                Browse Files
              </button>
            </div>
          </div>
        </div>

        {/* Results Section */}
        {loading && (
          <div className="mt-20 flex flex-col items-center animate-pulse">
            <Loader2 className="h-8 w-8 text-[#FF4D00] animate-spin mb-4" />
            <p className="font-bold tracking-tight text-slate-400 uppercase text-xs">
              Processing Lecture...
            </p>
          </div>
        )}

        {summary && (
          <div className="mt-24 bg-white border border-slate-200 rounded-3xl shadow-2xl shadow-slate-100 overflow-hidden animate-in fade-in slide-in-from-bottom-8">
            {/* 3. Update the Results Section to include the button and the ID */}
            <div className="flex items-center justify-between px-10 py-8 border-b border-slate-100 bg-slate-50/50">
              <div className="flex items-center space-x-3">
                <div className="bg-blue-100 p-2 rounded-full">
                  <CheckCircle className="h-5 w-5 text-blue-600" />
                </div>
                <h2 className="text-xl font-bold tracking-tighter uppercase text-slate-800">
                  Simplified Notes
                </h2>
              </div>
              <button
                onClick={downloadPDF}
                className="px-6 py-2 bg-[#FF4D00] text-white rounded-md text-sm font-bold hover:bg-orange-700 transition-all shadow-md shadow-orange-100"
              >
                Download PDF
              </button>
            </div>

            {/* This ID 'notes-content' is what the PDF generator looks for */}
            <div id="notes-content">
              <article className="px-12 py-16 prose prose-slate prose-lg max-w-none prose-headings:tracking-tighter prose-headings:font-bold">
                <ReactMarkdown>{summary}</ReactMarkdown>
              </article>
            </div>
          </div>
        )}
      </main>

      {/* Pure Footer - No Logo */}
      <footer className="border-t border-slate-100 py-12 px-8 flex justify-between items-center text-[10px] font-bold uppercase tracking-widest text-slate-400 mt-auto">
        <div>
          <p className="mb-1 text-slate-900 text-xs">Slide Sift.</p>
          <p>
            Transforming chaotic lecture slides into pristine, readable study
            guides.
          </p>
        </div>
        <p>© 2026 Slide Sift Inc.</p>
      </footer>
    </div>
  );
}
