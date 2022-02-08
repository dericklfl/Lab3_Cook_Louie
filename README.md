# Lab 3: Real-Time Scheduler and Motor Tasks

This lab utilizes the task files from the ME405 support repository to create tasks for driving the motors with the ability to run two motors simultaneously to different distances. 

---

### Step Response of System with Gain of 0.05 and Task Period of 10ms

![IdealGainResponse](/docs/10.png)

This is the step response obtained when using a gain of kP = 0.05 and a task period of 10ms.
This timing for the task gives the best results in the step response as there is no noticeable overshoot and it is not too slow.

---
### Step Response of System with Gain of 0.05 and Task Period of 30ms

![NonIdealGainResponse](/docs/30.png)

This is the step response obtained when using a gain of kP = 0.05 and a task period of 30ms.
With task timing at 30ms, the step response still remains fairly similar to the 10ms period response.

---
### Step Response of System with Gain of 0.05 and Task Period of 40ms

![NonIdealGainResponse](/docs/40.png)

This is the step response obtained when using a gain of kP = 0.05 and a task period of 40ms.
Once the task timing reaches 40ms, the step response becomes noticeably worse with a substantial overshoot. This period setting is too slow.

---
### Choosing a Proper Timing

When the task timing, or the period between runs of the task, is increased above 10ms there is a gradual decrease in quality of the motor's step response. When reaching 40ms period the step response shows a sizeable overshoot not present in faster periods.

---
