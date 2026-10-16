With 0.1.78 release it is now possible to use AC to try and develop custom AIs. An external app can connect to a few mapped memory files created by CSP to obtain current state of all cars and is expected to fill out new input state for all or just some of them. There are also functions allowing to control certain simulation aspects, like disable collisions between cars, slow down simulation, teleport cars around or restart the race.

Whole thing is in a bit of an experimental stage at the moment and only works for tracks that explicitly allow for custom AI to be applied in “surfaces.ini”. Just a temporary measure to make sure it wouldn’t mess up anything competitive at this stage with all those simulation-controlling options.

# Getting started

To activate custom AI:

- Open “assettocorsa/extension/config/new_behaviour.ini”, find `CUSTOM_AI` section and set `ENABLED` to 1. There are also other options you can use to speed up loading and overall performance if needed. (Also, make sure the entire “New Behavior” module is enabled as well.)

- Open “surfaces.ini” of a track you want to use it on, [activate extended physics](tracks-enabling-extended-physics.md) and then add `[_EXTRA_PERMISSIONS] ALLOW_CUSTOM_AI_MANIPULATION=1` to the same file.

# First steps

At the start, an external tool that wants to control a certain car should create a new memory mapped file called `AcTools.CSP.NewBehaviour.CustomAI.CarControls<N>.v0` (where `<N>` is 0-based car index) with a structure like this (filled with zeroes or something like that at the start):

```cpp
struct cai_car_controls {
  /* all structures are aligned by 4 bytes */

  float gas;
  float brake;
  float clutch;
  float steer; /* normalize steer value from -1 to 1 */
  float handbrake;

  bool gear_up; /* single byte value, 1 for true, 0 for false */
  bool gear_dn;
  bool drs;
  bool kers;

  bool brake_balance_up;
  bool brake_balance_dn;
  bool abs_up;
  bool abs_dn;

  bool tc_up;
  bool tc_dn;
  bool turbo_up;
  bool turbo_dn;

  bool engine_brake_up;
  bool engine_brake_dn;
  bool mguk_delivery_up;
  bool mguk_delivery_dn;

  bool mguk_recovery_up;
  bool mguk_recovery_dn;
  byte mguh_mode; /* unsigned char */
  bool headlights;

  byte teleport_to; /* set to 1 to teleport to pits, set to 2 to teleport to `teleport_pos` */
  bool autoclutch_on_start;
  bool autoclutch_on_change;
  bool autoblip_active;

  float3 teleport_pos; /* three floats, 12 bytes in total */
  float3 teleport_dir; /* note: wrongly inverted before 0.1.79 */

  bool autoshift_active;
}
```

It can be created after Assetto Corsa is launched, but once CSP would see it, it would quickly swap original car controller for that car with a custom one using data from that file as new car inputs. Data is read at 333 Hz, but it can be updated less often. And when it happens CSP would also create a new memory mapped file with a name like this: `AcTools.CSP.NewBehaviour.CustomAI.Car<N>.v0`. In that file CSP would provide detailed description of car state as `cai_car_data` structure (which would have four `cai_wheel_data` inside):

```cpp
struct cai_car_data {
  int packet_id; /* increments when updated */
  float gas;
  float brake;
  float clutch;
  float steer; /* steering angle in degrees */
  float handbrake;
  float fuel;
  int gear;
  float rpm;
  float speed_kmh;
  float3 velocity;
  float3 acc_g;  /* G-forces (Z is for acceleration force, X for left/right force) */
  float3 look;   /* car direction */
  float3 up;
  float3 position;
  float3 local_velocity;
  float3 local_angular_velocity;
  float cg_height;
  float car_damage[5];
  cai_wheel_data wheels[4];
  float turbo_boost;
  float final_ff;
  float final_pure_ff;
  bool pit_limiter;
  bool abs_in_action;
  bool traction_control_in_action;
  uint lap_time_ms;
  uint best_lap_time_ms;
  float drivetrain_torque;
  float spline_position;      /* position on AI spline (fast_lane.ai) */
  float collision_depth;      /* current collision depth in meters */
  uint collision_counter;     /* increments on collisions */
  uint wheels_valid_surface;  /* if Nth bit is set, Nth wheel is on valid
      track surface; 15 (1|2|4|8) if all wheels are on valid surface; added
      in 0.1.79. */
}

struct cai_wheel_data {
  float3 position;
  float3 contact_point;
  float3 contact_normal;
  float3 look;      /* wheel direction */
  float3 side;      /* vector pointing to wheel side */
  float3 velocity;  /* wheel velocity in world space */
  float slip_ratio;
  float load;
  float pressure;
  float angular_velocity;
  float wear;
  float dirty_level;
  float core_temperature;
  float camber_rad;
  float disc_temperature;
  float slip;
  float slip_angle_deg;
  float nd_slip;
};
```

So, to sum up, if an external app wishes to control second car in a simulation, it should:

- Create a new memory mapped file `AcTools.CSP.NewBehaviour.CustomAI.CarControls1.v0` with the size of `cai_car_controls` structure filled with zeroes (or maybe use 1 for brakes);
- Wait a bit for CSP to create `AcTools.CSP.NewBehaviour.CustomAI.Car1.v0`;
- If file is found, open it, map it and start a loop reading car state and outputting its controls;
- If file hasn’t been created, it might be because custom AI is not enabled, because track does not allow custom AIs or because that car can’t be controlled (such as remote cars online).

# Where are other cars

With custom AI active CSP would publish information about all the cars in `AcTools.CSP.NewBehaviour.CustomAI.CarPublic<N>.v0` files at 60 Hz (or whatever FPS is). That information is much more simplified (mostly because of how limited is data about remote cars online), but hopefully it should be enough for AIs:

```cpp
struct cai_car_public_data {
  int packet_id; /* increments when updated */
  float steer;
  float rpm;
  float spline_position;
  float speed_kmh;
  float3 velocity;
  float3 acc_g;
  float3 look;
  float3 up;
  float3 position;
  float car_damage[5];
  bool is_braking;
}
```

# Controlling simulation

To control the state of simulation, create a new file `AcTools.CSP.NewBehaviour.CustomAI.SimState.v0` and fill it with this structure:

```cpp
struct cai_sim_control {
  bool pause;               /* set to 1 to pause simulation */
  bool restart_session;     /* set to 1 to restart current session */
  bool disable_collisions;  /* if set to 1, collisions are disabled */
  byte extra_sleep_ms;      /* in case your AI in development needs some time to come up with answer,
                               this option can slow down the simulation */
};
```

Since 0.2.8, you can also control simulation time to speed things up with `AcTools.CSP.NewBehaviour.CustomAI.SimState.v1` (“v1” instead of “v0” to keep things compatible):

```cpp
struct cai_sim_control {
  bool pause;               /* set to 1 to pause simulation */
  bool restart_session;     /* set to 1 to restart current session */
  bool disable_collisions;  /* if set to 1, collisions are disabled */
  byte extra_sleep_ms;      /* in case your AI in development needs some time to come up with answer,
                               this option can slow down the simulation */
  float time_scale;         /* 1 for normal simulation time scale, increase to make time pass faster */
};
```

# Drawing debug lines

For debugging purposes you can also draw some debug lines. To do it, create a new file `AcTools.CSP.NewBehaviour.CustomAI.DebugLines.v0` with the size at least 16 KB and write this `cai_debug_lines` structure in it:

```cpp
struct cai_debug_lines {
  int count;
  cai_debug_line lines[count];
}

struct cai_debug_line {
  float3 from;
  float3 to;
  uint color;
}
```

# Example

[Here is a basic C# program showing how to connect, set some inputs, control sim state and draw debug lines](https://gist.github.com/gro-ove/11489f32b3eb3c9e3df1e7819bb3008e).
