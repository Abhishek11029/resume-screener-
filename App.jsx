import { useState } from 'react'
import UploadResumes from './components/UploadResumes'
import JobDescriptionInput from './components/JobDescriptionInput'
import Results from './components/Results'
import { rankResumes } from './api'

function App() {
  const [resumes, setResumes] = useState([])
  const [jobDescription, setJobDescription] = useState('')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleResumesUpload = (uploadedResumes) => {
    setResumes(uploadedResumes)
    setResults(null)
    setError(null)
  }

  const handleJobDescriptionChange = (description) => {
    setJobDescription(description)
    setResults(null)
    setError(null)
  }

  const handleRank = async () => {
    if (resumes.length === 0) {
      setError('Please upload at least one resume')
      return
    }
    if (!jobDescription.trim()) {
      setError('Please enter a job description')
      return
    }

    setLoading(true)
    setError(null)

    try {
      // First upload resumes
      const formData = new FormData()
      resumes.forEach((file) => {
        formData.append('files', file)
      })

      const uploadResponse = await fetch('http://localhost:8000/upload-resumes', {
        method: 'POST',
        body: formData,
      })

      if (!uploadResponse.ok) {
        throw new Error('Failed to upload resumes')
      }

      const uploadData = await uploadResponse.json()

      // Then submit job description
      const jobResponse = await fetch('http://localhost:8000/job-description', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ description: jobDescription }),
      })

      if (!jobResponse.ok) {
        throw new Error('Failed to submit job description')
      }

      // Finally rank resumes
      const rankData = await rankResumes()
      setResults(rankData)
    } catch (err) {
      setError(err.message || 'An error occurred while ranking resumes')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            AI Resume Screener
          </h1>
          <p className="text-gray-600">
            Upload resumes and job description to get AI-powered candidate rankings
          </p>
        </header>

        <div className="max-w-6xl mx-auto space-y-6">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <UploadResumes onUpload={handleResumesUpload} />
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6">
            <JobDescriptionInput
              value={jobDescription}
              onChange={handleJobDescriptionChange}
            />
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          <div className="text-center">
            <button
              onClick={handleRank}
              disabled={loading || resumes.length === 0 || !jobDescription.trim()}
              className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-semibold py-3 px-8 rounded-lg shadow-md transition duration-200"
            >
              {loading ? 'Ranking Resumes...' : 'Rank Resumes'}
            </button>
          </div>

          {results && (
            <div className="bg-white rounded-lg shadow-lg p-6">
              <Results results={results} />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App

