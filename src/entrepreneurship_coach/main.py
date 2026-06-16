#!/usr/bin/env python
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from entrepreneurship_coach.crews.dfv_crew.dfv_crew import dfv_crew



pes_lms = {
    "desirability": (
        "Undergraduate students at PES University face a major issue with missing internal assessment (ISA) deadlines. "
        "Because notifications are sent across multiple channels like WhatsApp, LMS, and Email, it causes administrative blindness for students. "
        "Consequently, students suffer a direct loss of 5-10% of their internal marks, which delays graduation or severely impacts final year placement eligibility. "
        "Tracking deadlines has become a daily active issue because PES recently increased the weightage of continuous evaluation."
    ),
    "feasibility": (
        "The proposed solution is an automated WhatsApp-based scraper that extracts personalized deadlines from the PES LMS and sends a daily morning 'Action Agenda'. "
        "The implementation is constrained such that the student team can build a basic Python scraper and use a local WhatsApp API wrapper without needing advanced infrastructure."
    ),
    "viability": (
        "The project was initially planned as a student subscription model, but since students are price-sensitive, "
        "it switched to a B2B2C model where anxious parents pay a small monthly fee of Rs. 100 to receive academic risk alerts about their ward's upcoming deadlines."
    ),

}

blnkt={
    
    "desirability":""" Analyze the following student project proposal:
        - Customer Problem: Urban consumers need immediate access to groceries and essentials without spending time traveling to stores
        - Target Audience: Millennials, Gen Z, busy professionals, and students in metro cities aged 18-40
        - Key Value Proposition: 10-minute delivery guarantee, real-time order tracking, wide product selection
        - User Pain Points Solved: Time savings, convenience for impulse purchases, avoids crowded stores
        - Market Demand Indicators: High adoption rate in urban India, 4.2+ app rating, repeat usage frequency
        - Emotional Drivers: Convenience, instant gratification, time flexibility
                                          """, 
                                          
                                          
                                          
                                          
        "feasibility":""" The following is a startup/project idea submitted by a user:
            - Technology Stack: React Native mobile apps, cloud infrastructure, inventory management systems, route optimization algorithms
            - Infrastructure Model: Dark stores (micro-warehouses) located 2-3km from target customers, 500+ sq ft each
            - Logistics: Proprietary delivery fleet of 5,000+ delivery partners with GPS tracking
            - Supply Chain: Partnerships with 10,000+ local retailers and wholesale distributors
            - Operational Capabilities: Real-time demand forecasting, automated inventory replenishment, dynamic routing
            - Technical Challenges: Inventory accuracy, delivery time optimization, peak-hour scalability, cold chain for perishables
            - Resource Requirements: Capital investment for dark store network, technology development team, delivery workforce""", 
                                          
                                          
                                          
                                          
      "viability":""" 
        Analyze the business viability of the following project proposal:
        - Revenue Model: 
          * Delivery fees (₹29-₹59 per order)
          * Platform commissions from sellers (15-25%)
          * Advertising fees from brands
          * Blinkit Prime membership (₹99/month)
        
        - Cost Structure:
          * Dark store operational costs (rent, staffing, inventory)
          * Delivery partner payments (₹40-₹60 per delivery)
          * Technology and infrastructure costs
          * Marketing and customer acquisition costs
        
        - Market Size: India quick commerce market = $3B in 2024, projected $5-7B by 2025
        - Unit Economics: Average order value ₹300-₹500, order frequency 2-3 times/week per customer
        - Competitive Position: Market leader in 10-minute delivery, competes with Swiggy Instamart, Zepto, BigBasket
        - Profitability Status: Contribution margin positive as of 2024 (reported by Zomato)
        - Growth Trajectory: 300+ cities, 50M+ active users, 20% monthly growth
        """
        ,
}

sncc={
    "desirability":
    """SNACCED is a proposed quick-service food delivery platform that aims to deliver snacks, beverages, and light meals within 10–15 minutes. The idea is designed to address a common problem faced by students, office workers, and busy urban consumers who often want quick refreshments but are discouraged by the longer delivery times associated with traditional food delivery services.
    Modern consumers increasingly value convenience and instant access to products and services. The growth of quick-commerce platforms suggests that customer expectations are shifting toward faster fulfillment. SNACCED could capitalize on this trend by focusing specifically on snack-sized orders and impulse purchases.
    Existing food delivery services often prioritize full meals, leaving a gap for customers seeking smaller, faster, and more affordable food options. By offering a curated menu optimized for rapid delivery, SNACCED could provide a more suitable solution for these use cases.
    """,
    "feasibility":"""SNACCED can be developed using existing technologies and operational models. The platform would require a mobile application, inventory management systems, demand forecasting tools, route optimization software, and a network of delivery partners.
    To achieve rapid delivery times, SNACCED could operate through strategically located micro-fulfillment centers or dark stores stocked with high-demand snack items and beverages. This approach would reduce preparation time and enable faster order fulfillment.
    Several operational challenges would need to be addressed, including inventory management, maintaining product freshness, minimizing wastage, and ensuring delivery consistency during peak demand periods. Scaling operations across multiple locations would also require careful planning and investment.
    Despite these challenges, the required technology and infrastructure already exist in the market, making implementation realistic for a startup or established company.
    """,
    "viability":"""SNACCED could generate revenue through delivery fees, product markups, subscription plans, promotional partnerships, and advertising opportunities. Its primary customer segments would likely include students, young professionals, office workers, and urban consumers seeking convenience.
    However, the business model faces challenges related to profitability. Snack and beverage orders typically have lower average order values compared to full meal orders. At the same time, maintaining a rapid delivery network requires investment in infrastructure, inventory, delivery personnel, and technology.
    To improve financial sustainability, SNACCED could focus on high-density urban areas, encourage larger basket sizes through combo offerings, and integrate subscription-based benefits that increase customer retention and order frequency.
    Long-term success would depend on balancing customer convenience with operational efficiency while maintaining healthy profit margins.
    """,
}


qubi = {
        "desirability":
    """Quibi was a mobile-first video streaming platform launched in 2020 that offered short-form, premium content designed for consumption in episodes of 10 minutes or less. The platform aimed to serve busy consumers who wanted high-quality entertainment during short breaks, commutes, and daily routines.
    Although the concept appeared attractive, Quibi struggled to create sufficient demand among its target audience. Consumers already had access to free short-form content on platforms such as YouTube, TikTok, and Instagram. Many users did not perceive enough additional value to justify paying for another streaming subscription.
    Furthermore, Quibi launched during the COVID-19 pandemic when commuting and travel activities declined significantly, reducing situations where its content format was most useful. The platform also lacked social sharing features, limiting user engagement and organic growth.
    """,
    "feasibility":"""From a technical perspective, Quibi was highly feasible. The company successfully developed a mobile streaming platform capable of delivering high-quality video content. It introduced innovative features such as Turnstyle, which allowed users to seamlessly switch between portrait and landscape viewing modes.
    Quibi was supported by experienced leadership, significant financial backing, and partnerships with major content creators and production studios. The platform infrastructure, content delivery systems, and user experience functioned as intended.
    While content production required substantial resources, there were no major technological barriers preventing implementation or operation.
    """,
    "viability":"""Quibi faced significant challenges in establishing a sustainable business model. The platform relied primarily on subscription revenue while investing heavily in original content production. Billions of dollars were spent on creating exclusive shows and acquiring talent.
    However, subscriber growth remained far below expectations. Customer acquisition costs were high, and user retention was weak. Since users did not perceive enough value compared to free alternatives, revenue growth failed to keep pace with operational expenses.
    Additionally, the competitive streaming market made it difficult for Quibi to secure a long-term position. Established platforms such as Netflix, YouTube, and emerging short-form video platforms offered stronger value propositions and larger user bases.
    As a result, Quibi struggled to achieve profitability and could not sustain its business operations.
    """,

    }

ggls= {
            "desirability":
    """Google Glass was introduced as a wearable smart device that allowed users to access information, capture photos and videos, navigate locations, and receive notifications through a heads-up display. The product aimed to bring augmented reality and hands-free computing into everyday life.
    Although the technology generated significant excitement during its launch, widespread consumer demand never fully materialized. Many potential users struggled to identify a compelling everyday use case that justified purchasing the device. In addition, privacy concerns emerged because the built-in camera could record others without their knowledge. This led to social discomfort and negative public perception, with some establishments even banning the device.
    The design also faced criticism for being intrusive and awkward in social settings. As a result, consumers viewed Google Glass more as a technological novelty than a must-have product.
    """,
    "feasibility":"""Google Glass represented an ambitious technological achievement, but several technical limitations affected its practicality. The device faced challenges related to battery life, processing power, heat generation, display quality, and overall user comfort.
    The hardware required users to balance functionality with wearability, making it difficult to deliver a seamless experience. Extended use often resulted in battery drain, and the device's limited capabilities restricted its usefulness compared to smartphones.
    Additionally, the technology ecosystem for augmented reality applications was still immature at the time of launch. Developers had limited opportunities to create compelling applications that could fully leverage the platform.
    Although the device functioned as intended, the technology was not sufficiently advanced to support a mass-market consumer product.
     """,
    "viability":"""Google Glass was launched at a premium price of approximately $1,500, making it inaccessible to most consumers. The high cost, combined with limited functionality and uncertain demand, created significant barriers to adoption.
    The product required substantial investment in research, development, manufacturing, and ecosystem development. However, sales remained relatively low, preventing Google from achieving the scale necessary to justify continued expansion of the consumer version.
    Without widespread adoption, it became difficult to attract developers, create a thriving application ecosystem, and generate sustainable revenue. As a result, the consumer-focused version of Google Glass was discontinued.
    Interestingly, Google later repositioned Glass toward enterprise and industrial use cases, where hands-free access to information offered clearer business value.
    """,}

class coach_flow(Flow):

    @start()
    def dfv(self):
        print("Kickoff the Crew")
        from datetime import datetime
        today = datetime.now().strftime("%d - %B - %Y")
        output = (
            dfv_crew()
            .crew()
            .kickoff(inputs={**qubi, "TodayDate": today})
        )
        print(output.raw)


    # @listen(dfv)
    # def generate_content(self):
    #     print(f"Generating content on: {self.state.topic}")
    #     result = (
    #         ContentCrew()
    #         .crew()
    #         .kickoff(inputs={"topic": self.state.topic})
    #     )


def kickoff():
    content_flow = coach_flow()
    content_flow.kickoff()


def plot():
    content_flow = coach_flow()
    content_flow.plot()


if __name__ == "__main__":
    kickoff()
