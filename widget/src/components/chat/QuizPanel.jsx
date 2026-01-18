import React, { useState } from 'react';

/**
 * QuizPanel Component
 * Interactive quiz interface for testing knowledge
 * Can be displayed in compact or expanded mode
 */
export const QuizPanel = ({ isExpanded = false }) => {
  const [quizzes] = useState([
    {
      id: 1,
      title: 'Chapter 1: Fundamentals',
      questions: 10,
      completed: 8,
      score: 80,
      status: 'in-progress',
    },
    {
      id: 2,
      title: 'Midterm Review',
      questions: 20,
      completed: 20,
      score: 85,
      status: 'completed',
    },
    {
      id: 3,
      title: 'Practice Quiz 3',
      questions: 15,
      completed: 0,
      score: 0,
      status: 'not-started',
    },
  ]);

  const [currentQuiz, setCurrentQuiz] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [showResult, setShowResult] = useState(false);

  // Sample quiz data
  const sampleQuizData = {
    id: 1,
    title: 'Chapter 1: Fundamentals',
    questions: [
      {
        id: 1,
        question: 'What is the primary purpose of active learning techniques?',
        options: [
          'To memorize information faster',
          'To engage with material and enhance retention',
          'To complete assignments quickly',
          'To avoid studying altogether',
        ],
        correctAnswer: 1,
        explanation: 'Active learning techniques help engage with the material more deeply, which enhances long-term retention and understanding.',
      },
      {
        id: 2,
        question: 'Which of the following is an example of spaced repetition?',
        options: [
          'Studying all night before an exam',
          'Reviewing material at increasing intervals',
          'Reading the textbook once',
          'Highlighting important passages',
        ],
        correctAnswer: 1,
        explanation: 'Spaced repetition involves reviewing material at gradually increasing intervals, which is proven to improve long-term retention.',
      },
    ],
  };

  const handleStartQuiz = (quiz) => {
    setCurrentQuiz(sampleQuizData);
    setCurrentQuestion(0);
    setSelectedAnswer(null);
    setShowResult(false);
  };

  const handleAnswerSelect = (index) => {
    setSelectedAnswer(index);
  };

  const handleSubmitAnswer = () => {
    setShowResult(true);
  };

  const handleNextQuestion = () => {
    if (currentQuestion < currentQuiz.questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
      setSelectedAnswer(null);
      setShowResult(false);
    } else {
      setCurrentQuiz(null);
      setCurrentQuestion(0);
      setSelectedAnswer(null);
      setShowResult(false);
    }
  };

  const handleBackToList = () => {
    setCurrentQuiz(null);
    setCurrentQuestion(0);
    setSelectedAnswer(null);
    setShowResult(false);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return { bg: '#DCFCE7', text: '#166534' };
      case 'in-progress':
        return { bg: '#FEF3C7', text: '#854D0E' };
      default:
        return { bg: '#F3F4F6', text: '#6B7280' };
    }
  };

  const getStatusLabel = (status) => {
    switch (status) {
      case 'completed':
        return 'Completed';
      case 'in-progress':
        return 'In Progress';
      default:
        return 'Not Started';
    }
  };

  // Quiz taking view
  if (currentQuiz) {
    const question = currentQuiz.questions[currentQuestion];
    const isCorrect = selectedAnswer === question.correctAnswer;

    return (
      <div style={{ 
        height: isExpanded ? 'calc(90vh - 80px)' : '100%', 
        display: 'flex', 
        flexDirection: 'column',
        background: isExpanded ? '#FFFFFF' : 'transparent',
        borderRadius: isExpanded ? '0' : '0'
      }}>
        {/* Quiz Header */}
        <div style={{ padding: '16px', borderBottom: '1px solid #E5E7EB', background: '#FFFFFF' }}>
          <button
            onClick={handleBackToList}
            style={{
              padding: '6px 12px',
              borderRadius: '8px',
              border: '1px solid #E5E7EB',
              background: '#FFFFFF',
              color: '#6B7280',
              fontSize: '13px',
              fontWeight: '500',
              cursor: 'pointer',
              marginBottom: '12px',
            }}
          >
            ← Back to Quizzes
          </button>
          <h3 style={{ 
            fontSize: '16px', 
            fontWeight: '600',
            color: '#111827',
            marginBottom: '8px',
          }}>
            {currentQuiz.title}
          </h3>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            fontSize: '13px',
            color: '#6B7280',
          }}>
            <span>Question {currentQuestion + 1} of {currentQuiz.questions.length}</span>
            <div style={{
              flex: 1,
              height: '6px',
              background: '#F3F4F6',
              borderRadius: '3px',
              overflow: 'hidden',
            }}>
              <div style={{
                width: `${((currentQuestion + 1) / currentQuiz.questions.length) * 100}%`,
                height: '100%',
                background: 'linear-gradient(235deg, #8629FF 0%, #FF1F38 80%)',
                transition: 'width 0.3s',
              }} />
            </div>
          </div>
        </div>

        {/* Question */}
        <div style={{ 
          flex: 1, 
          overflowY: 'auto',
          padding: isExpanded ? '32px 24px' : '24px 16px',
          background: isExpanded ? '#F9FAFB' : '#FFFFFF',
        }}>
          <div style={{
            maxWidth: isExpanded ? '800px' : '100%',
            margin: isExpanded ? '0 auto' : '0',
          }}>
            <h4 style={{
              fontSize: isExpanded ? '18px' : '16px',
              fontWeight: '600',
              color: '#111827',
              lineHeight: '1.5',
              marginBottom: '24px',
            }}>
              {question.question}
            </h4>

            {/* Options */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {question.options.map((option, index) => {
                const isSelected = selectedAnswer === index;
                const showCorrectness = showResult;
                const isThisCorrect = index === question.correctAnswer;
                
                let borderColor = '#E5E7EB';
                let background = '#FFFFFF';
                
                if (showCorrectness) {
                  if (isSelected && isCorrect) {
                    borderColor = '#10B981';
                    background = '#DCFCE7';
                  } else if (isSelected && !isCorrect) {
                    borderColor = '#EF4444';
                    background = '#FEE2E2';
                  } else if (isThisCorrect) {
                    borderColor = '#10B981';
                    background = '#DCFCE7';
                  }
                } else if (isSelected) {
                  borderColor = '#8629FF';
                  background = '#EEEBFF';
                }

                return (
                  <button
                    key={index}
                    onClick={() => !showResult && handleAnswerSelect(index)}
                    disabled={showResult}
                    style={{
                      padding: '16px',
                      borderRadius: '12px',
                      border: `2px solid ${borderColor}`,
                      background,
                      textAlign: 'left',
                      cursor: showResult ? 'default' : 'pointer',
                      transition: 'all 0.2s',
                      fontSize: '14px',
                      color: '#374151',
                      fontWeight: '500',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '12px',
                    }}
                  >
                    <div style={{
                      width: '24px',
                      height: '24px',
                      borderRadius: '50%',
                      border: `2px solid ${borderColor}`,
                      background: isSelected || (showCorrectness && isThisCorrect) 
                        ? borderColor 
                        : '#FFFFFF',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      flexShrink: 0,
                      color: '#FFFFFF',
                      fontSize: '12px',
                      fontWeight: '600',
                    }}>
                      {showCorrectness && isThisCorrect && '✓'}
                      {showCorrectness && isSelected && !isCorrect && '✗'}
                    </div>
                    <span>{option}</span>
                  </button>
                );
              })}
            </div>

            {/* Explanation */}
            {showResult && (
              <div style={{
                padding: '16px',
                borderRadius: '12px',
                background: isCorrect ? '#DCFCE7' : '#FEF3C7',
                border: `1px solid ${isCorrect ? '#10B981' : '#F59E0B'}`,
                marginTop: '20px',
              }}>
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  marginBottom: '8px',
                }}>
                  <span style={{ fontSize: '18px' }}>
                    {isCorrect ? '✅' : '💡'}
                  </span>
                  <h5 style={{
                    fontSize: '14px',
                    fontWeight: '600',
                    color: isCorrect ? '#166534' : '#854D0E',
                  }}>
                    {isCorrect ? 'Correct!' : 'Not quite'}
                  </h5>
                </div>
                <p style={{
                  fontSize: '13px',
                  color: isCorrect ? '#166534' : '#854D0E',
                  lineHeight: '1.5',
                }}>
                  {question.explanation}
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Actions */}
        <div style={{
          padding: '16px',
          borderTop: '1px solid #E5E7EB',
          display: 'flex',
          gap: '12px',
          background: '#FFFFFF',
        }}>
          {!showResult ? (
            <button
              onClick={handleSubmitAnswer}
              disabled={selectedAnswer === null}
              style={{
                flex: 1,
                padding: '12px',
                borderRadius: '10px',
                border: 'none',
                background: selectedAnswer !== null
                  ? 'linear-gradient(235deg, #8629FF 0%, #FF1F38 80%)'
                  : '#E5E7EB',
                color: '#FFFFFF',
                fontSize: '14px',
                fontWeight: '500',
                cursor: selectedAnswer !== null ? 'pointer' : 'not-allowed',
              }}
            >
              Submit Answer
            </button>
          ) : (
            <button
              onClick={handleNextQuestion}
              style={{
                flex: 1,
                padding: '12px',
                borderRadius: '10px',
                border: 'none',
                background: 'linear-gradient(235deg, #8629FF 0%, #FF1F38 80%)',
                color: '#FFFFFF',
                fontSize: '14px',
                fontWeight: '500',
                cursor: 'pointer',
              }}
            >
              {currentQuestion < currentQuiz.questions.length - 1 
                ? 'Next Question' 
                : 'Finish Quiz'}
            </button>
          )}
        </div>
      </div>
    );
  }

  // Quiz list view
  return (
    <div style={{ 
      height: isExpanded ? 'calc(90vh - 80px)' : '100%', 
      display: 'flex', 
      flexDirection: 'column',
      background: isExpanded ? '#F9FAFB' : '#FFFFFF'
    }}>
      {/* Header */}
      <div style={{ 
        padding: isExpanded ? '20px 24px' : '16px', 
        borderBottom: '1px solid #E5E7EB',
        background: '#FFFFFF'
      }}>
        <h3 style={{ 
          fontSize: isExpanded ? '20px' : '18px', 
          fontWeight: '600',
          color: '#111827',
          marginBottom: '4px',
        }}>
          Quiz
        </h3>
        <p style={{ 
          fontSize: '13px', 
          color: '#6B7280' 
        }}>
          Test your knowledge
        </p>
      </div>

      {/* Quiz List */}
      <div style={{ 
        flex: 1, 
        overflowY: 'auto',
        padding: isExpanded ? '24px' : '16px',
      }}>
        <div style={{ 
          display: 'grid',
          gridTemplateColumns: isExpanded ? 'repeat(auto-fill, minmax(350px, 1fr))' : '1fr',
          gap: '16px',
          maxWidth: isExpanded ? 'none' : '100%'
        }}>
          {quizzes.map(quiz => {
            const statusColors = getStatusColor(quiz.status);
            const progress = (quiz.completed / quiz.questions) * 100;

            return (
              <div
                key={quiz.id}
                style={{
                  padding: '16px',
                  background: '#FFFFFF',
                  border: '1px solid #E5E7EB',
                  borderRadius: '12px',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.borderColor = '#8629FF';
                  e.currentTarget.style.boxShadow = '0 2px 8px rgba(134, 41, 255, 0.15)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.borderColor = '#E5E7EB';
                  e.currentTarget.style.boxShadow = 'none';
                }}
              >
                {/* Header */}
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'flex-start',
                  marginBottom: '12px',
                }}>
                  <h4 style={{ 
                    fontSize: '14px', 
                    fontWeight: '600',
                    color: '#111827',
                    flex: 1,
                  }}>
                    {quiz.title}
                  </h4>
                  <span style={{
                    padding: '4px 8px',
                    borderRadius: '6px',
                    background: statusColors.bg,
                    color: statusColors.text,
                    fontSize: '11px',
                    fontWeight: '500',
                    whiteSpace: 'nowrap',
                    marginLeft: '8px',
                  }}>
                    {getStatusLabel(quiz.status)}
                  </span>
                </div>

                {/* Stats */}
                <div style={{
                  display: 'flex',
                  gap: '16px',
                  marginBottom: '12px',
                  fontSize: '13px',
                  color: '#6B7280',
                }}>
                  <span>📝 {quiz.questions} questions</span>
                  {quiz.status !== 'not-started' && (
                    <span>📊 Score: {quiz.score}%</span>
                  )}
                </div>

                {/* Progress Bar */}
                {quiz.status !== 'not-started' && (
                  <div style={{
                    marginBottom: '12px',
                  }}>
                    <div style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      marginBottom: '4px',
                      fontSize: '12px',
                      color: '#6B7280',
                    }}>
                      <span>Progress</span>
                      <span>{quiz.completed}/{quiz.questions}</span>
                    </div>
                    <div style={{
                      height: '6px',
                      background: '#F3F4F6',
                      borderRadius: '3px',
                      overflow: 'hidden',
                    }}>
                      <div style={{
                        width: `${progress}%`,
                        height: '100%',
                        background: 'linear-gradient(235deg, #8629FF 0%, #FF1F38 80%)',
                        transition: 'width 0.3s',
                      }} />
                    </div>
                  </div>
                )}

                {/* Action Button */}
                <button
                  onClick={() => handleStartQuiz(quiz)}
                  style={{
                    width: '100%',
                    padding: '10px',
                    borderRadius: '8px',
                    border: 'none',
                    background: quiz.status === 'completed' 
                      ? '#F3F4F6' 
                      : '#EEEBFF',
                    color: quiz.status === 'completed' 
                      ? '#6B7280' 
                      : '#8629FF',
                    fontSize: '13px',
                    fontWeight: '500',
                    cursor: 'pointer',
                    marginTop: '8px',
                  }}
                >
                  {quiz.status === 'completed' 
                    ? 'Review Quiz' 
                    : quiz.status === 'in-progress' 
                      ? 'Continue Quiz' 
                      : 'Start Quiz'}
                </button>
              </div>
            );
          })}
        </div>
      </div>

      {/* Generate Quiz Button */}
      <div style={{
        padding: '16px',
        borderTop: '1px solid #E5E7EB',
        background: '#FFFFFF',
      }}>
        <button style={{
          width: '100%',
          padding: '12px',
          borderRadius: '10px',
          border: 'none',
          background: 'linear-gradient(235deg, #8629FF 0%, #FF1F38 80%)',
          color: '#FFFFFF',
          fontSize: '14px',
          fontWeight: '500',
          cursor: 'pointer',
        }}>
          ✨ Generate New Quiz
        </button>
      </div>
    </div>
  );
};

export default QuizPanel;