function JobDescriptionInput({ value, onChange }) {
  return (
    <div>
      <h2 className="text-2xl font-semibold text-gray-800 mb-4">
        Job Description
      </h2>
      <p className="text-gray-600 mb-4">
        Paste or type the job description you want to match resumes against
      </p>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Enter job description here... Include requirements, skills needed, experience level, education requirements, etc."
        className="w-full h-64 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-none"
      />
      <div className="mt-2 text-sm text-gray-500">
        {value.length} characters
      </div>
    </div>
  )
}

export default JobDescriptionInput

