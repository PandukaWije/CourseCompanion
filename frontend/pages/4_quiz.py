"""
Quiz Page - Course Assessment Interface
"""
import streamlit as st
import sys
sys.path.append("..")

from utils.api_client import APIClient

st.set_page_config(page_title="Quiz - CourseCompanion", page_icon="📝", layout="wide")

def init_quiz_state():
    """Initialize quiz-specific state"""
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False

def get_quiz_questions(course_id: str) -> list:
    """Get quiz questions for a course"""
    # Mock quiz data - in production, fetch from API
    quizzes = {
        "xm-cloud-101": [
            {
                "id": "q1",
                "question": "What is the primary purpose of XM Cloud?",
                "options": [
                    "Database management",
                    "Headless content management and delivery",
                    "Email marketing",
                    "Customer relationship management"
                ],
                "correct": 1,
                "topic": "fundamentals"
            },
            {
                "id": "q2", 
                "question": "Which framework is commonly used with XM Cloud for frontend development?",
                "options": [
                    "Angular only",
                    "Vue.js only",
                    "Next.js with JSS",
                    "PHP"
                ],
                "correct": 2,
                "topic": "development"
            },
            {
                "id": "q3",
                "question": "What does 'headless' mean in the context of XM Cloud?",
                "options": [
                    "No user interface at all",
                    "Content is separated from presentation",
                    "Only works without a database",
                    "Requires no authentication"
                ],
                "correct": 1,
                "topic": "architecture"
            },
            {
                "id": "q4",
                "question": "How are components typically created in XM Cloud?",
                "options": [
                    "Only through the UI",
                    "Using SQL scripts",
                    "As React/Next.js components with Sitecore integration",
                    "Through XML configuration only"
                ],
                "correct": 2,
                "topic": "development"
            },
            {
                "id": "q5",
                "question": "What is the deployment model for XM Cloud?",
                "options": [
                    "On-premise only",
                    "SaaS (Software as a Service)",
                    "Self-hosted required",
                    "Desktop application"
                ],
                "correct": 1,
                "topic": "deployment"
            }
        ],
        "search-fundamentals": [
            {
                "id": "q1",
                "question": "What is the primary function of an index in Sitecore Search?",
                "options": [
                    "Store user passwords",
                    "Enable fast content retrieval",
                    "Manage user sessions",
                    "Handle authentication"
                ],
                "correct": 1,
                "topic": "indexing"
            },
            {
                "id": "q2",
                "question": "What are facets in search?",
                "options": [
                    "Error messages",
                    "Categories for filtering search results",
                    "Database tables",
                    "User permissions"
                ],
                "correct": 1,
                "topic": "facets"
            },
            {
                "id": "q3",
                "question": "What is boosting in search queries?",
                "options": [
                    "Making searches slower",
                    "Increasing relevance of certain results",
                    "Removing results",
                    "Encrypting queries"
                ],
                "correct": 1,
                "topic": "optimization"
            },
            {
                "id": "q4",
                "question": "When should you rebuild a search index?",
                "options": [
                    "Never",
                    "After significant content changes or schema updates",
                    "Every minute",
                    "Only on weekends"
                ],
                "correct": 1,
                "topic": "indexing"
            }
        ],
        "content-hub-101": [
            {
                "id": "q1",
                "question": "What is the primary use case for Content Hub DAM?",
                "options": [
                    "Code deployment",
                    "Digital asset management",
                    "User authentication",
                    "Email sending"
                ],
                "correct": 1,
                "topic": "dam"
            },
            {
                "id": "q2",
                "question": "What does CMP stand for in Content Hub?",
                "options": [
                    "Code Management Platform",
                    "Content Marketing Platform",
                    "Customer Management Portal",
                    "Central Media Player"
                ],
                "correct": 1,
                "topic": "cmp"
            },
            {
                "id": "q3",
                "question": "How do workflows help in Content Hub?",
                "options": [
                    "They slow down processes",
                    "They automate content review and approval processes",
                    "They delete content automatically",
                    "They prevent any changes"
                ],
                "correct": 1,
                "topic": "workflows"
            },
            {
                "id": "q4",
                "question": "What types of assets can Content Hub manage?",
                "options": [
                    "Only images",
                    "Only videos",
                    "Multiple asset types including images, videos, documents",
                    "Only PDFs"
                ],
                "correct": 2,
                "topic": "dam"
            },
            {
                "id": "q5",
                "question": "What is the benefit of Content Hub's integration capabilities?",
                "options": [
                    "It cannot integrate with other systems",
                    "It enables connection with other marketing and content tools",
                    "It only works standalone",
                    "Integration removes all features"
                ],
                "correct": 1,
                "topic": "integration"
            }
        ]
    }
    
    return quizzes.get(course_id, [])

def check_enrollment():
    """Check if user has selected courses"""
    if not st.session_state.get("selected_courses"):
        st.warning("⚠️ You haven't selected any courses yet!")
        if st.button("📚 Go to Landing Page"):
            st.switch_page("pages/1_landing.py")
        return False
    return True

def render_quiz_selection():
    """Render quiz course selection"""
    st.markdown("### Select a Course to Take the Quiz")
    
    course_names = {
        "xm-cloud-101": "XM Cloud Fundamentals",
        "search-fundamentals": "Sitecore Search Fundamentals",
        "content-hub-101": "Content Hub Basics"
    }
    
    for course_id in st.session_state.selected_courses:
        name = course_names.get(course_id, course_id)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**📖 {name}**")
            questions = get_quiz_questions(course_id)
            st.caption(f"{len(questions)} questions")
        with col2:
            if st.button("Start Quiz", key=f"start_{course_id}"):
                st.session_state.quiz_course = course_id
                st.session_state.quiz_started = True
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
                st.rerun()
        
        st.markdown("---")

def render_quiz_questions():
    """Render quiz questions"""
    course_id = st.session_state.quiz_course
    questions = get_quiz_questions(course_id)
    
    course_names = {
        "xm-cloud-101": "XM Cloud Fundamentals",
        "search-fundamentals": "Sitecore Search Fundamentals",
        "content-hub-101": "Content Hub Basics"
    }
    
    st.markdown(f"### 📝 Quiz: {course_names.get(course_id, course_id)}")
    st.markdown(f"*{len(questions)} questions*")
    
    if st.button("← Back to Quiz Selection"):
        st.session_state.quiz_started = False
        st.rerun()
    
    st.markdown("---")
    
    with st.form("quiz_form"):
        for i, q in enumerate(questions):
            st.markdown(f"**Question {i + 1}: {q['question']}**")
            
            answer = st.radio(
                "Select your answer:",
                options=range(len(q['options'])),
                format_func=lambda x, opts=q['options']: opts[x],
                key=f"quiz_q_{q['id']}",
                index=st.session_state.quiz_answers.get(q['id'], 0)
            )
            
            st.session_state.quiz_answers[q['id']] = answer
            st.markdown("---")
        
        submitted = st.form_submit_button("📤 Submit Quiz", use_container_width=True)
        
        if submitted:
            # Calculate score
            score = 0
            results = []
            topic_scores = {}
            
            for q in questions:
                user_answer = st.session_state.quiz_answers.get(q['id'], -1)
                is_correct = user_answer == q['correct']
                
                if is_correct:
                    score += 1
                
                results.append({
                    "question_id": q['id'],
                    "question": q['question'],
                    "user_answer": user_answer,
                    "correct_answer": q['correct'],
                    "is_correct": is_correct,
                    "topic": q['topic']
                })
                
                # Track topic scores
                if q['topic'] not in topic_scores:
                    topic_scores[q['topic']] = {"correct": 0, "total": 0}
                topic_scores[q['topic']]["total"] += 1
                if is_correct:
                    topic_scores[q['topic']]["correct"] += 1
            
            # Store results
            st.session_state.quiz_results[course_id] = {
                "score": score,
                "total": len(questions),
                "percentage": (score / len(questions)) * 100,
                "results": results,
                "topic_scores": topic_scores
            }
            
            st.session_state.quiz_submitted = True
            st.success(f"🎉 Quiz submitted! Score: {score}/{len(questions)} ({(score/len(questions)*100):.0f}%)")
            
            if st.button("📊 View Detailed Results"):
                st.switch_page("pages/5_results.py")

def render_sidebar():
    """Render quiz page sidebar"""
    with st.sidebar:
        st.markdown("### 📝 Quiz Tips")
        st.markdown("""
        - Read each question carefully
        - Review all options before selecting
        - You can change answers before submitting
        - Take your time!
        """)
        
        st.markdown("---")
        
        if st.session_state.quiz_started:
            st.markdown("### 📊 Progress")
            questions = get_quiz_questions(st.session_state.quiz_course)
            answered = len(st.session_state.quiz_answers)
            st.progress(answered / len(questions) if questions else 0)
            st.caption(f"{answered}/{len(questions)} answered")

def main():
    """Main page function"""
    init_quiz_state()
    render_sidebar()
    
    st.title("📝 Course Quiz")
    
    if not check_enrollment():
        return
    
    if st.session_state.quiz_started:
        render_quiz_questions()
    else:
        render_quiz_selection()

if __name__ == "__main__":
    main()





