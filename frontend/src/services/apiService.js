/**
 * API Service Layer for Maharashtra Skill Intelligence Platform
 * Supports both Live FastAPI backend calls and Mock Data fallback.
 * Allows switching to real APIs without modifying page components.
 */

import dashboardData from '../data/dashboardData';
import districtData from '../data/districtData';
import skillGapData from '../data/skillGapData';
import courseAlignmentData from '../data/courseAlignmentData';
import trainingPlanData from '../data/trainingPlanData';

// When backend is ready, set VITE_API_BASE_URL='http://localhost:8000' in .env
const API_BASE_URL = import.meta.env?.VITE_API_BASE_URL || '';
const USE_MOCK = !API_BASE_URL;

// Helper to simulate network latency for realistic loading states
const simulateDelay = (ms = 180) => new Promise(resolve => setTimeout(resolve, ms));

export const apiService = {
  /**
   * Fetches high-level executive dashboard metrics, state KPIs, and top gaps.
   */
  async getDashboard() {
    if (USE_MOCK) {
      await simulateDelay();
      return dashboardData;
    }
    const response = await fetch(`${API_BASE_URL}/api/dashboard`);
    if (!response.ok) throw new Error(`Dashboard API error: ${response.statusText}`);
    return await response.json();
  },

  /**
   * Fetches list of all 5 supported Maharashtra districts.
   */
  async getDistricts() {
    if (USE_MOCK) {
      await simulateDelay();
      return [
        { id: 'Pune', name: 'Pune', region: 'Western Maharashtra', focus: 'Automotive & IT Hub' },
        { id: 'Mumbai', name: 'Mumbai', region: 'Konkan', focus: 'Finance, Tech & Logistics' },
        { id: 'Nagpur', name: 'Nagpur', region: 'Vidarbha', focus: 'Logistics & MIHAN Cluster' },
        { id: 'Nashik', name: 'Nashik', region: 'North Maharashtra', focus: 'Auto Ancillaries & Precision Eng' },
        { id: 'Chhatrapati Sambhajinagar', name: 'Chhatrapati Sambhajinagar', region: 'Marathwada', focus: 'Auto & AURIC Smart City' }
      ];
    }
    const response = await fetch(`${API_BASE_URL}/api/districts`);
    if (!response.ok) throw new Error(`Districts API error: ${response.statusText}`);
    return await response.json();
  },

  /**
   * Fetches detailed district industrial & job market analysis.
   * @param {string} districtId - District name or ID (e.g. 'Pune')
   */
  async getDistrictAnalysis(districtId = 'Pune') {
    if (USE_MOCK) {
      await simulateDelay();
      const district = districtData.districts[districtId];
      if (!district) throw new Error(`District '${districtId}' not found.`);
      return district;
    }
    const response = await fetch(`${API_BASE_URL}/api/districts/${encodeURIComponent(districtId)}`);
    if (!response.ok) throw new Error(`District analysis API error: ${response.statusText}`);
    return await response.json();
  },

  /**
   * Fetches skill gap intelligence for a specific district and/or skill.
   * @param {string} skillId - Optional skill name or ID filter
   * @param {string} districtId - Optional district filter
   */
  async getSkillGap(skillId = null, districtId = null) {
    if (USE_MOCK) {
      await simulateDelay();
      let records = skillGapData.all_gap_records;

      if (districtId && districtId !== 'ALL') {
        records = records.filter(r => r.district.toLowerCase() === districtId.toLowerCase());
      }
      if (skillId) {
        records = records.filter(r => 
          r.skill.toLowerCase().includes(skillId.toLowerCase()) || 
          r.skill_id.toLowerCase() === skillId.toLowerCase()
        );
      }
      return {
        priority_thresholds: skillGapData.priority_thresholds,
        priority_distribution: skillGapData.priority_distribution,
        statewide_summary: skillGapData.statewide_summary,
        records: records
      };
    }
    const params = new URLSearchParams();
    if (skillId) params.append('skill', skillId);
    if (districtId && districtId !== 'ALL') params.append('district', districtId);
    const response = await fetch(`${API_BASE_URL}/api/skills/gaps?${params.toString()}`);
    if (!response.ok) throw new Error(`Skill gap API error: ${response.statusText}`);
    return await response.json();
  },

  /**
   * Fetches course alignment, effectiveness score, and curriculum gaps.
   * @param {string} courseId - Optional course ID (e.g. 'C001')
   */
  async getCourse(courseId = null) {
    if (USE_MOCK) {
      await simulateDelay();
      if (courseId) {
        const course = courseAlignmentData.courses.find(c => c.course_id === courseId);
        if (!course) throw new Error(`Course '${courseId}' not found.`);
        return course;
      }
      return courseAlignmentData.courses;
    }
    const url = courseId ? `${API_BASE_URL}/api/courses/${courseId}` : `${API_BASE_URL}/api/courses/alignment`;
    const response = await fetch(url);
    if (!response.ok) throw new Error(`Course API error: ${response.statusText}`);
    return await response.json();
  },

  /**
   * Fetches targeted recommendations for a given district or skill.
   */
  async getRecommendations(districtId = 'Pune', skillId = null) {
    if (USE_MOCK) {
      await simulateDelay();
      const plan = trainingPlanData.district_plans[districtId];
      if (!plan) throw new Error(`Training plan for '${districtId}' not found.`);
      return {
        district: districtId,
        expansions: plan.action_plan.course_expansions,
        modernizations: plan.action_plan.curriculum_modernizations,
        new_courses: plan.action_plan.new_courses_to_introduce,
        targeted_seats: plan.action_plan.targeted_additional_seats
      };
    }
    const params = new URLSearchParams({ district: districtId });
    if (skillId) params.append('skill', skillId);
    const response = await fetch(`${API_BASE_URL}/api/recommendations?${params.toString()}`);
    if (!response.ok) throw new Error(`Recommendations API error: ${response.statusText}`);
    return await response.json();
  },

  /**
   * Fetches actionable District Training Plan roadmap.
   * @param {string} districtId - District name
   */
  async getTrainingPlan(districtId = 'Pune') {
    if (USE_MOCK) {
      await simulateDelay();
      if (!districtId || districtId === 'STATEWIDE') {
        return trainingPlanData;
      }
      const plan = trainingPlanData.district_plans[districtId];
      if (!plan) throw new Error(`District training plan for '${districtId}' not found.`);
      return {
        district: districtId,
        state_summary: trainingPlanData.state_summary,
        plan: plan
      };
    }
    const response = await fetch(`${API_BASE_URL}/api/training-plans/${encodeURIComponent(districtId)}`);
    if (!response.ok) throw new Error(`Training plan API error: ${response.statusText}`);
    return await response.json();
  }
};

export default apiService;

