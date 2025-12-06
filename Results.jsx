function Results({ results }) {
  if (!results || !results.rankings) {
    return <div>No results available</div>
  }

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600 bg-green-100'
    if (score >= 60) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  const getScoreBarColor = (score) => {
    if (score >= 80) return 'bg-green-500'
    if (score >= 60) return 'bg-yellow-500'
    return 'bg-red-500'
  }

  return (
    <div>
      <h2 className="text-2xl font-semibold text-gray-800 mb-6">
        Ranking Results
      </h2>

      <div className="space-y-6">
        {results.rankings.map((candidate, index) => (
          <div
            key={candidate.resume_id}
            className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-4">
                <div className="flex items-center justify-center w-12 h-12 bg-indigo-100 text-indigo-600 rounded-full font-bold text-lg">
                  #{index + 1}
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-gray-800">
                    {candidate.filename || `Resume ${index + 1}`}
                  </h3>
                  <p className="text-sm text-gray-500">
                    Resume ID: {candidate.resume_id}
                  </p>
                </div>
              </div>
              <div
                className={`px-4 py-2 rounded-full font-bold text-lg ${getScoreColor(
                  candidate.total_score
                )}`}
              >
                {candidate.total_score.toFixed(1)}%
              </div>
            </div>

            {/* Score Breakdown */}
            <div className="mb-4">
              <h4 className="text-sm font-semibold text-gray-700 mb-2">
                Score Breakdown
              </h4>
              <div className="space-y-2">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-600">Skills Match (40%)</span>
                    <span className="font-medium">
                      {candidate.scores.skill_match.toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full ${getScoreBarColor(
                        candidate.scores.skill_match
                      )}`}
                      style={{
                        width: `${candidate.scores.skill_match}%`,
                      }}
                    ></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-600">
                      Semantic Similarity (30%)
                    </span>
                    <span className="font-medium">
                      {candidate.scores.semantic_similarity.toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full ${getScoreBarColor(
                        candidate.scores.semantic_similarity
                      )}`}
                      style={{
                        width: `${candidate.scores.semantic_similarity}%`,
                      }}
                    ></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-600">
                      Experience Relevance (20%)
                    </span>
                    <span className="font-medium">
                      {candidate.scores.experience_match.toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full ${getScoreBarColor(
                        candidate.scores.experience_match
                      )}`}
                      style={{
                        width: `${candidate.scores.experience_match}%`,
                      }}
                    ></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-600">
                      Education/Projects (10%)
                    </span>
                    <span className="font-medium">
                      {candidate.scores.education_projects.toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full ${getScoreBarColor(
                        candidate.scores.education_projects
                      )}`}
                      style={{
                        width: `${candidate.scores.education_projects}%`,
                      }}
                    ></div>
                  </div>
                </div>
              </div>
            </div>

            {/* Strengths & Weaknesses */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <h4 className="text-sm font-semibold text-green-700 mb-2">
                  Strengths
                </h4>
                <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                  {candidate.strengths && candidate.strengths.length > 0 ? (
                    candidate.strengths.map((strength, i) => (
                      <li key={i}>{strength}</li>
                    ))
                  ) : (
                    <li className="text-gray-400">No specific strengths identified</li>
                  )}
                </ul>
              </div>
              <div>
                <h4 className="text-sm font-semibold text-red-700 mb-2">
                  Weaknesses
                </h4>
                <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                  {candidate.weaknesses && candidate.weaknesses.length > 0 ? (
                    candidate.weaknesses.map((weakness, i) => (
                      <li key={i}>{weakness}</li>
                    ))
                  ) : (
                    <li className="text-gray-400">No major weaknesses identified</li>
                  )}
                </ul>
              </div>
            </div>

            {/* Summary */}
            {candidate.summary && (
              <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                <h4 className="text-sm font-semibold text-gray-700 mb-2">
                  Summary
                </h4>
                <p className="text-sm text-gray-600">{candidate.summary}</p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default Results

