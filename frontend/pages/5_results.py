"""
Results Page - Quiz Results and Recommendations
"""
import streamlit as st
import sys
sys.path.append("..")

from utils.api_client import APIClient

st.set_page_config(page_title="Results - CourseCompanion", page_icon="📊", layout="wide")

def check_results():
    """Check if there are quiz results to display"""
    if not st.session_state.get("quiz_results"):
        st.info("📝 No quiz results yet!")
        st.markdown("Complete a quiz to see your results and personalized recommendations.")
        
        if st.button("📝 Take a Quiz"):
            st.switch_page("pages/4_quiz.py")
        return False
    return True

def render_score_overview(results: dict, course_name: str):
    """Render the score overview section"""
    score = results["score"]
    total = results["total"]
    percentage = results["percentage"]
    
    st.markdown(f"### 📊 {course_name}")
    
    # Score display
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Score", f"{score}/{total}")
    
    with col2:
        st.metric("Percentage", f"{percentage:.0f}%")
    
    with col3:
        if percentage >= 80:
            st.metric("Status", "✅ Passed")
        elif percentage >= 60:
            st.metric("Status", "⚠️ Needs Review")
        else:
            st.metric("Status", "❌ Needs Work")
    
    # Progress bar with color
    if percentage >= 80:
        st.success(f"Excellent! You've mastered this course!")
    elif percentage >= 60:
        st.warning(f"Good effort! Review the weak areas below.")
    else:
        st.error(f"Keep learning! Check the recommendations below.")
    
    st.progress(percentage / 100)

def render_topic_breakdown(results: dict):
    """Render topic-by-topic breakdown"""
    st.markdown("### 📈 Topic Performance")
    
    topic_scores = results.get("topic_scores", {})
    
    if not topic_scores:
        st.info("No topic breakdown available")
        return
    
    # Create columns for topic cards
    cols = st.columns(min(len(topic_scores), 3))
    
    for i, (topic, scores) in enumerate(topic_scores.items()):
        col_idx = i % len(cols)
        with cols[col_idx]:
            correct = scores["correct"]
            total = scores["total"]
            pct = (correct / total * 100) if total > 0 else 0
            
            # Color based on performance
            if pct >= 80:
                st.success(f"**{topic.replace('_', ' ').title()}**")
            elif pct >= 50:
                st.warning(f"**{topic.replace('_', ' ').title()}**")
            else:
                st.error(f"**{topic.replace('_', ' ').title()}**")
            
            st.caption(f"{correct}/{total} correct ({pct:.0f}%)")

def render_question_review(results: dict):
    """Render detailed question review"""
    st.markdown("### 📋 Question Review")
    
    with st.expander("View All Questions", expanded=False):
        for i, result in enumerate(results.get("results", [])):
            is_correct = result["is_correct"]
            
            if is_correct:
                st.success(f"**Q{i+1}: {result['question']}** ✅")
            else:
                st.error(f"**Q{i+1}: {result['question']}** ❌")
                st.caption(f"Your answer was incorrect. Topic: {result['topic']}")
            
            st.markdown("---")

def generate_recommendations(results: dict, course_id: str) -> list:
    """Generate personalized recommendations based on quiz results"""
    recommendations = []
    topic_scores = results.get("topic_scores", {})
    
    # Course-specific recommendations
    course_recommendations = {
        "xm-cloud-101": {
            "fundamentals": {
                "module": "Module 1: Introduction to XM Cloud",
                "artifact": "mindmap",
                "tip": "Review the core concepts and architecture overview"
            },
            "development": {
                "module": "Module 4: Component Development",
                "artifact": "slides",
                "tip": "Practice creating components with the JSS SDK"
            },
            "architecture": {
                "module": "Module 2: Architecture Overview",
                "artifact": "mindmap",
                "tip": "Study the headless architecture diagram"
            },
            "deployment": {
                "module": "Module 5: Deployment & Publishing",
                "artifact": "summary",
                "tip": "Follow the deployment checklist step by step"
            }
        },
        "search-fundamentals": {
            "indexing": {
                "module": "Module 1 & 2: Search Architecture & Indexing",
                "artifact": "mindmap",
                "tip": "Understand when and how to rebuild indexes"
            },
            "facets": {
                "module": "Module 4: Faceted Search",
                "artifact": "slides",
                "tip": "Practice creating facet configurations"
            },
            "optimization": {
                "module": "Module 3: Query Optimization",
                "artifact": "summary",
                "tip": "Learn about boosting and relevance tuning"
            }
        },
        "content-hub-101": {
            "dam": {
                "module": "Module 2: Asset Management",
                "artifact": "mindmap",
                "tip": "Explore different asset types and metadata"
            },
            "cmp": {
                "module": "Module 3: Content Operations",
                "artifact": "slides",
                "tip": "Understand the content lifecycle"
            },
            "workflows": {
                "module": "Module 5: Workflows & Approvals",
                "artifact": "summary",
                "tip": "Practice creating approval workflows"
            },
            "integration": {
                "module": "Module 4: Integration Patterns",
                "artifact": "slides",
                "tip": "Review API documentation and examples"
            }
        }
    }
    
    course_recs = course_recommendations.get(course_id, {})
    
    # Find weak topics (below 70%)
    for topic, scores in topic_scores.items():
        pct = (scores["correct"] / scores["total"] * 100) if scores["total"] > 0 else 0
        
        if pct < 70:
            rec = course_recs.get(topic, {
                "module": f"Review {topic.replace('_', ' ').title()} section",
                "artifact": "summary",
                "tip": f"Focus on {topic.replace('_', ' ')} concepts"
            })
            
            recommendations.append({
                "topic": topic,
                "score": pct,
                "priority": "high" if pct < 50 else "medium",
                **rec
            })
    
    # Sort by score (lowest first)
    recommendations.sort(key=lambda x: x["score"])
    
    return recommendations

def render_recommendations(recommendations: list, course_id: str):
    """Render personalized recommendations"""
    st.markdown("### 🎯 Personalized Recommendations")
    
    if not recommendations:
        st.success("🎉 Great job! You've shown strong understanding across all topics!")
        st.markdown("Consider taking the next course in the learning path or exploring advanced topics.")
        return
    
    st.markdown("Based on your quiz results, here are areas to focus on:")
    
    for rec in recommendations:
        priority_icon = "🔴" if rec["priority"] == "high" else "🟡"
        
        with st.expander(f"{priority_icon} **{rec['topic'].replace('_', ' ').title()}** - {rec['score']:.0f}% score", expanded=True):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**📖 Suggested Module:** {rec['module']}")
                st.markdown(f"**💡 Tip:** {rec['tip']}")
            
            with col2:
                artifact_type = rec.get("artifact", "summary")
                if st.button(f"View {artifact_type.title()}", key=f"rec_{rec['topic']}"):
                    st.session_state.current_course = course_id
                    st.session_state.requested_artifact = artifact_type
                    st.switch_page("pages/3_learning.py")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📖 Return to Learning", use_container_width=True):
            st.switch_page("pages/3_learning.py")
    with col2:
        if st.button("🔄 Retake Quiz", use_container_width=True):
            st.switch_page("pages/4_quiz.py")

def render_sidebar():
    """Render results page sidebar"""
    with st.sidebar:
        st.markdown("### 📊 Results Summary")
        
        if st.session_state.get("quiz_results"):
            for course_id, results in st.session_state.quiz_results.items():
                course_names = {
                    "xm-cloud-101": "XM Cloud",
                    "search-fundamentals": "Search",
                    "content-hub-101": "Content Hub"
                }
                name = course_names.get(course_id, course_id)
                pct = results["percentage"]
                
                if pct >= 80:
                    st.success(f"✅ {name}: {pct:.0f}%")
                elif pct >= 60:
                    st.warning(f"⚠️ {name}: {pct:.0f}%")
                else:
                    st.error(f"❌ {name}: {pct:.0f}%")
        
        st.markdown("---")
        st.markdown("### 🎯 Next Steps")
        st.markdown("""
        - Review weak areas
        - Check recommended modules
        - Access learning artifacts
        - Retake quiz if needed
        """)

def main():
    """Main page function"""
    render_sidebar()
    
    st.title("📊 Quiz Results & Recommendations")
    
    if not check_results():
        return
    
    # Course name mapping
    course_names = {
        "xm-cloud-101": "XM Cloud Fundamentals",
        "search-fundamentals": "Sitecore Search Fundamentals",
        "content-hub-101": "Content Hub Basics"
    }
    
    # If multiple courses have results, let user select
    result_courses = list(st.session_state.quiz_results.keys())
    
    if len(result_courses) > 1:
        selected_course = st.selectbox(
            "Select Course Results",
            result_courses,
            format_func=lambda x: course_names.get(x, x)
        )
    else:
        selected_course = result_courses[0]
    
    results = st.session_state.quiz_results[selected_course]
    course_name = course_names.get(selected_course, selected_course)
    
    st.markdown("---")
    
    # Render all sections
    render_score_overview(results, course_name)
    
    st.markdown("---")
    
    render_topic_breakdown(results)
    
    st.markdown("---")
    
    recommendations = generate_recommendations(results, selected_course)
    render_recommendations(recommendations, selected_course)
    
    st.markdown("---")
    
    render_question_review(results)

if __name__ == "__main__":
    main()





