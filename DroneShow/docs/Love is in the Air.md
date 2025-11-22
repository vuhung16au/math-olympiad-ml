https://gemini.google.com/app/8dc545ddd29500b4

---

For a major drone show like **Vivid Sydney 2024 ("Love is in the Air")**, the minimum safety distance between two drones typically falls between **1.5 and 3 meters**.

While the exact distance depends on the specific drone model and wind conditions, the industry standards for safety are broken down below.

### 1. Minimum Distance Between Drones (Inter-Drone Spacing)
This is the "collision avoidance" distance programmed into the swarm software to ensure drones don't hit each other due to wind gusts or GPS drift.
* **Typical Distance:** **2 meters to 2.5 meters** is the industry standard for large fleets (like the 700+ drones used in Vivid).
* **Advanced Capability:** High-end commercial fleets (using RTK-GPS for centimeter-level precision) can fly as close as **1.5 meters** to create high-resolution shapes, but this is riskier in windy harbor environments like Circular Quay.
* **Why this distance?** Drones create "downwash" (turbulent air pushed downwards). If one drone flies too close *below* or *beside* another, this turbulence can destabilize it, causing it to drop or crash.

### 2. Distance From the Audience (CASA Regulations)
In Australia, safety is strictly regulated by the Civil Aviation Safety Authority (CASA). For a show like Vivid, the safety buffers are much larger than the space between drones:
* **Horizontal Buffer:** The drone swarm must be at least **30 meters** away from any person (audience). For large shows, this exclusion zone often extends to **100+ meters** to account for potential drift.
* **Vertical Buffer:** Drones are usually not allowed to fly directly over people.
* **Geofencing:** The show uses a "Virtual Fence." If a drone crosses this invisible line (due to wind or malfunction), it is instantly powered down to fall into a designated "kill zone" (usually the water in Sydney Harbour) rather than flying towards the crowd.

### Summary for Vivid Sydney 2024
* **Show:** "Love is in the Air" (June 2024)
* **Fleet Size:** 700+ drones
* **Estimated Spacing:** ~2 meters between drones
* **Tech Provider:** Likely used **Nova Sky Stories** (formerly Intel) or similar commercially certified heavy-duty swarm drones, which are designed to hold position within centimeters even in the harbour breeze.

---

Based on deep research into Vivid Sydney's 2024 "Love is in the Air" show, here are the specific technical findings you can use to build a realistic simulation.

### 1. Show Specifications (Input Data)
To simulate this specific show, your environment needs to support these parameters:
* **Fleet Size:** 700+ drones.
* **Technology Provider:** **Australian Traffic Network (ATN)** provided the drone technology (likely using a proprietary fleet management system similar to SPH Engineering's *Drone Show Software*).
* **Key Visuals (Choreography):**
    * **Theme:** Romantic love ("Love is in the Air").
    * **Formations:** "Universal symbols of love" (Hearts, Cupid, Rings), plus a giant "Nova Boy" character (due to sponsorship by Nova Entertainment).
    * **Color Palette:** RGB LEDs capable of full spectrum, but heavily reliant on Reds, Pinks, and Golds for this theme.

### 2. Collision Avoidance Strategy (For your Algorithm)
Unlike consumer drones (like DJI Mavics) that use sensors to "see" and avoid obstacles, light show drones rely on **determinism**.
* **Finding:** The show does *not* rely on active collision avoidance sensors (e.g., LIDAR/Sonar) on each drone during the show.
* **Simulation Logic:**
    1.  **Pre-flight Validation:** The collision avoidance happens *before* takeoff. The software checks the entire timeline of 700 flight paths to ensure no two paths ever cross within a set radius.
    2.  **RTK GPS:** In your simulation, assume "Perfect Positioning." Real drones use Real-Time Kinematic (RTK) GPS to stay within 1-2cm of their programmed path.
    3.  **Synchronized Clocks:** All drones operate on a centralized time-code. If one drone lags, it is often programmed to "land immediately" rather than try to catch up and risk collision.

### 3. Safety Parameters (The "Rules" for your Sim)
To make your simulation "safe" by Australian standards, apply these constraints to your physics engine:

| Parameter | Value | Note for Simulation |
| :--- | :--- | :--- |
| **Min Inter-Drone Distance** | **2.5 Meters** | If distance < 2.5m, flag as a "Collision Risk". High-end shows push to 1.5m, but 2.5m is the standard safe buffer. |
| **Max Flight Speed** | **3 - 5 m/s** | Limit your drone velocity. Faster speeds require larger separation distances. |
| **Max Altitude** | **120 Meters** | CASA regulation limit (400ft). |
| **Geofence (Hard)** | **Virtual Box** | Create a bounding box. If a simulated drone crosses this line, it should instantly drop (simulating a "kill switch"). |
| **Crowd Buffer** | **30 Meters** | Horizontal distance from the takeoff/show zone to the nearest "audience" camera view. |

### 4. Recommended Tools to Simulate This
If you want to recreate this on your computer today, these are the industry-standard tools used to design exactly this type of show:

**Option A: The "Pro" Standard (Commercial)**
* **Software:** **Drone Show Software (DSS)** by SPH Engineering.
* **Workflow:** This is what actual show designers use. It has a built-in plugin for **Blender**. You animate in Blender, and DSS validates the safety.

**Option B: The "Open Source" Way (Best for Learning)**
* **Software:** **Skybrush Studio** (Blender Plugin).
* **Why:** It is free and open-source.
* **How to use it:**
    1.  Install **Blender** (3D animation software).
    2.  Install the **Skybrush Studio** plugin.
    3.  Set your "Safety Parameters" in the Skybrush panel to the values listed above (2.5m distance, 3m/s speed).
    4.  Animate your 700 dots (drones) to form a heart.
    5.  Run the "Safety Check" script—it will highlight red any time two drones get too close, allowing you to fix the choreography.

---

**Yes, the drones physically move.**

They are not a stationary "grid" of lights like a TV screen. Instead, they physically fly from one position to another to build each shape in the sky.

Here is the specific breakdown of how they performed the **"Love is in the Air"** show:

### 1. The "Move and Freeze" Technique
The show follows a repetitive cycle to keep the audience safe and the visuals crisp:
1.  **Lights OFF (Transition):** The drones turn off their LEDs (or dim them) and fly to their new coordinates. This hides the messy "swarming" movement from the audience.
2.  **Lights ON (Formation):** Once they reach their exact spot (using RTK GPS), they stop, hover in place, and turn their lights on to reveal the new shape (e.g., the Heart or Cupid).
3.  **Animation (Micro-Movements):** While holding the shape, they perform small movements to animate it.
    * *Example:* In "Love is in the Air," the drones likely didn't just form a static heart; they might have physically moved in and out to make the heart "beat."

### 2. Exception: The "Pixel" Effect
There is one exception where they *do* just flash lights like you guessed.
* If the drones form a dense "screen" or "grid" in the sky, they can stay still and flash different colors to create a scrolling text or a changing image.
* However, this requires a huge number of drones to get good resolution. Since "Love is in the Air" had ~700 drones, they mostly relied on **physical movement** to create outlines of shapes (vector graphics) rather than solid screens (raster graphics).

### Summary for your Simulation
If you are building a simulation, **do not** build a static grid. You need to program **Waypoints**:
* **State A:** Drones form a Heart at coordinates $(x_1, y_1, z_1)$.
* **Action:** Drones calculate a path to coordinates $(x_2, y_2, z_2)$.
* **State B:** Drones arrive and form a Ring.