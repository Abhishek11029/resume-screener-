const API_BASE_URL = 'http://localhost:8000'

export const uploadResumes = async (files) => {
  const formData = new FormData()
  files.forEach((file) => {
    formData.append('files', file)
  })

  const response = await fetch(`${API_BASE_URL}/upload-resumes`, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    throw new Error('Failed to upload resumes')
  }

  return response.json()
}

export const submitJobDescription = async (description) => {
  const response = await fetch(`${API_BASE_URL}/job-description`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ description }),
  })

  if (!response.ok) {
    throw new Error('Failed to submit job description')
  }

  return response.json()
}

export const rankResumes = async () => {
  const response = await fetch(`${API_BASE_URL}/rank`, {
    method: 'POST',
  })

  if (!response.ok) {
    throw new Error('Failed to rank resumes')
  }

  return response.json()
}

export const getReport = async (resumeId) => {
  const response = await fetch(`${API_BASE_URL}/report/${resumeId}`)

  if (!response.ok) {
    throw new Error('Failed to get report')
  }

  return response.json()
}

