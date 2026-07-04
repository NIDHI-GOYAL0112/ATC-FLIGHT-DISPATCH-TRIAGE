import collections
import collections.abc
collections.Mapping = collections.abc.Mapping  

from experta import *

# --- HELPER FUNCTION FOR KNOWLEDGE BASE ---
def is_weather_safe(aircraft, wind, vis, weather):
    """
    Evaluates if the weather is safe based on aircraft size, visibility, 
    and dynamically calculates wind limits based on runway conditions.
    """
    if weather == "Thunderstorm": return False
    if vis < 0.5: return False 
    if weather == "Fog" and vis < 1.0: return False

    wind_penalty = 0
    if weather in ["Heavy Rain", "Snow / Ice"]:
        wind_penalty = 5  

    if aircraft == "Small" and wind > (20 - wind_penalty): return False
    if aircraft == "Medium" and wind > (30 - wind_penalty): return False
    if aircraft in ["Large", "Industrial", "Army"] and wind > (40 - wind_penalty): return False
    
    return True


# --- 1. EXPERT SYSTEM FACTS ---
class FlightData(Fact):
    pass

class WeatherStatus(Fact):
    pass

class FuelStatus(Fact):
    pass

class AircraftPriority(Fact):
    pass


# --- 2. THE INFERENCE ENGINE ---
class DispatchTriage(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.verdict = []

    # --- TIER 1: DEDUCING WEATHER CONDITIONS ---
    @Rule(FlightData(aircraft=MATCH.a, wind_knots=MATCH.w, visibility_miles=MATCH.v, weather_type=MATCH.wt),
          TEST(lambda a, w, v, wt: not is_weather_safe(a, w, v, wt)))
    def weather_severe(self):
        self.declare(WeatherStatus(level="Severe"))
        self.verdict.append("🌩️ HAZARD: Weather exceeds safe operating limits (Check crosswind limits or visibility).")

    @Rule(FlightData(aircraft=MATCH.a, wind_knots=MATCH.w, visibility_miles=MATCH.v, weather_type=MATCH.wt),
          TEST(lambda a, w, v, wt: is_weather_safe(a, w, v, wt)))
    def weather_clear(self):
        self.declare(WeatherStatus(level="Clear"))
        self.verdict.append("🌤️ WEATHER: Conditions are within safe limits for this aircraft.")

    # --- TIER 1: SPECIAL WEATHER RULES ---
    @Rule(FlightData(weather_type="Snow / Ice"))
    def winter_operations(self):
        self.verdict.append("❄️ RUNWAY ALERT: Snow/Ice detected. Runway friction reduced. De-icing equipment must be on standby.")

    @Rule(FlightData(weather_type="Thunderstorm"))
    def severe_convection(self):
        self.verdict.append("⚡ WARNING: Thunderstorm cell detected. High risk of microbursts and wind shear.")

    # --- TIER 1: DEDUCING FUEL STATUS ---
    @Rule(FlightData(fuel_mins=MATCH.f), TEST(lambda f: f < 45))
    def fuel_critical(self):
        self.declare(FuelStatus(level="Critical"))
        self.verdict.append("⛽ FUEL ALERT: Aircraft is operating on critical reserve fuel (< 45 mins).")

    @Rule(FlightData(fuel_mins=MATCH.f), TEST(lambda f: f >= 45))
    def fuel_healthy(self):
        self.declare(FuelStatus(level="Healthy"))
        self.verdict.append("⛽ FUEL: Sufficient holding fuel available.")

    # --- TIER 1: SPECIAL MILITARY CLEARANCE ---
    @Rule(FlightData(aircraft="Army"))
    def army_priority(self):
        self.declare(AircraftPriority(status="Military"))
        self.verdict.append("🎖️ PRIORITY: Military aircraft detected. Expediting ATC routing.")

    # --- TIER 2: FINAL DISPATCH DECISIONS (Fact Chaining) ---
    @Rule(WeatherStatus(level="Severe"), FuelStatus(level="Healthy"))
    def action_hold_pattern(self):
        self.verdict.append("✈️ FINAL ACTION: INITIATE HOLDING PATTERN. Circle the destination until the weather front passes.")

    @Rule(WeatherStatus(level="Severe"), FuelStatus(level="Critical"))
    def action_divert(self):
        self.verdict.append("🚨 FINAL ACTION: EMERGENCY DIVERSION. Reroute immediately to the nearest alternate airport.")

    @Rule(WeatherStatus(level="Clear"))
    def action_land(self):
        self.verdict.append("🛬 FINAL ACTION: CLEARED FOR APPROACH. Proceed with standard landing protocols.")


# --- 3. COMMAND LINE INTERFACE ---
def run_cli():
    print("\n=============================================")
    print("   ATC Flight Dispatch Triage (Expert System)  ")
    print("=============================================\n")
    
    try:
        # 1. Aircraft Selection
        print("Select Aircraft Class:")
        print("  [1] Small (e.g., Cessna)")
        print("  [2] Medium (e.g., Regional Jet)")
        print("  [3] Large (e.g., Commercial Airliner)")
        print("  [4] Industrial (e.g., Heavy Cargo)")
        print("  [5] Army (e.g., Military Transport)")
        
        while True:
            plane_choice = int(input("Enter choice (1-5): "))
            if 1 <= plane_choice <= 5: break
            print("  -> Invalid. Please select a number between 1 and 5.")
            
        plane_categories = {1: "Small", 2: "Medium", 3: "Large", 4: "Industrial", 5: "Army"}
        plane = plane_categories[plane_choice]
        
        # 2. Weather Selection
        print("\nSelect Current Destination Weather:")
        print("  [1] Clear / Normal")
        print("  [2] Light Rain")
        print("  [3] Heavy Rain")
        print("  [4] Snow / Ice")
        print("  [5] Thunderstorm")
        print("  [6] Fog")
        
        while True:
            weather_choice = int(input("Enter choice (1-6): "))
            if 1 <= weather_choice <= 6: break
            print("  -> Invalid. Please select a number between 1 and 6.")
            
        weather_categories = {
            1: "Clear / Normal", 2: "Light Rain", 3: "Heavy Rain", 
            4: "Snow / Ice", 5: "Thunderstorm", 6: "Fog"
        }
        weather = weather_categories[weather_choice]

        # 3. Telemetry Input (With strict boundary validation)
        print(f"\n--- Entering telemetry for {plane} Aircraft in {weather} ---")
        
        while True:
            fuel = int(input("Fuel Remaining (0 - 1200 mins): "))
            if 0 <= fuel <= 1200: break
            print("  -> Error: Fuel must be between 0 and 1200 minutes.")

        while True:
            vis = float(input("Visibility (0.0 - 50.0 miles):  "))
            if 0.0 <= vis <= 50.0: break
            print("  -> Error: Visibility must be between 0.0 and 50.0 miles.")

        while True:
            wind = int(input("Wind Speed (0 - 200 knots):     "))
            if 0 <= wind <= 200: break
            print("  -> Error: Wind speed must be between 0 and 200 knots.")

    except ValueError:
        print("\n[Critical Error] Input crashed. Please ensure you only type numbers, not letters.")
        return

    print("\n[ Processing Telemetry through Inference Engine... ]\n")

    # Initialize and run
    engine = DispatchTriage()
    engine.reset()
    engine.declare(FlightData(
        aircraft=plane,
        fuel_mins=fuel, 
        visibility_miles=vis, 
        wind_knots=wind,
        weather_type=weather
    ))
    engine.run()

    # Output results
    if len(engine.verdict) == 0:
        print("🔍 System Notice: Telemetry unclassified. Requires manual dispatcher review.")
    else:
        for item in engine.verdict:
            print(item)
            
    print("\n=============================================\n")


if __name__ == "__main__":
    run_cli()