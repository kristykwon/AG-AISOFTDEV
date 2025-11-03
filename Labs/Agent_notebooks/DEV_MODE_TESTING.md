# 🧪 Dev Mode Testing Checklist

## Quick Test Steps

### Test 1: Toggle Functionality
1. ✅ Open http://localhost:8001
2. ✅ Locate the "🔧 Dev Mode" toggle switch
3. ✅ Click the toggle to turn it ON
4. ✅ Verify status message: "🔧 Dev mode enabled - Detailed logging active"
5. ✅ Click the toggle to turn it OFF
6. ✅ Verify the toggle switches state properly

### Test 2: Dev Mode OFF (Default Behavior)
1. ✅ Ensure dev mode toggle is OFF
2. ✅ Enter a business problem (or use an example)
3. ✅ Click "Generate PRD"
4. ✅ Observe: Status updates only (no detailed logs)
5. ✅ Verify: Clean output, no dev logs panel visible
6. ✅ Wait for PRD to complete

**Expected Result:**
- Status bar shows progress messages
- No dev logs panel appears
- PRD generates normally
- Faster execution (no verbose logging overhead)

### Test 3: Dev Mode ON (Verbose Logging)
1. ✅ Turn dev mode toggle ON
2. ✅ Clear the output if needed
3. ✅ Enter a business problem
4. ✅ Click "Generate PRD"
5. ✅ Observe the **Dev Logs** panel appears
6. ✅ Watch real-time logs streaming:
   - 🤖 Agent initialization logs
   - 📋 Task execution logs
   - ✅ Result/milestone logs
7. ✅ Verify auto-scrolling (logs scroll automatically)
8. ✅ Check timestamps on each log entry
9. ✅ Wait for completion

**Expected Result:**
- Dev logs panel visible above output
- Real-time log entries with timestamps
- Different colored logs (agent/task/result)
- Clear visibility into what's happening
- PRD generates successfully

### Test 4: Log Types Verification
**Check that you see logs from all three types:**

#### 🤖 Agent Logs (Blue)
- "Creating Requirements Analyst agent..."
- "Creating Product Manager agent..."
- "Creating QA Reviewer agent..."
- "Crew assembled with 3 agents..."

#### 📋 Task Logs (Yellow)
- "Task 1: Requirements Analyst analyzing..."
- "Task 2: Product Manager synthesizing..."
- "Task 3: QA Reviewer validating..."

#### ✅ Result Logs (Green)
- "Executing CrewAI workflow - This may take 60-120 seconds..."
- "Crew execution completed! Processing output..."

### Test 5: Performance Comparison

**Test A - Dev Mode OFF:**
1. Start timer when clicking "Generate PRD"
2. Note time when PRD completes
3. Record time: _____ seconds

**Test B - Dev Mode ON:**
1. Start timer when clicking "Generate PRD"
2. Note time when PRD completes
3. Record time: _____ seconds

**Expected:**
- Dev Mode OFF: ~60-90 seconds
- Dev Mode ON: ~65-100 seconds (5-10% overhead)

### Test 6: UI/UX Validation

**Toggle Switch:**
- ✅ Visually appealing
- ✅ Clear ON/OFF state
- ✅ Smooth animation
- ✅ Blue when enabled
- ✅ Gray when disabled

**Dev Logs Panel:**
- ✅ Dark theme (black background)
- ✅ Monospace font
- ✅ Scrollable (max 300px height)
- ✅ Auto-scroll to latest log
- ✅ Timestamp on each entry
- ✅ Colored by log type
- ✅ Icons match log type

**Overall Layout:**
- ✅ Toggle doesn't break layout
- ✅ Logs panel fits nicely above output
- ✅ No horizontal scrolling needed
- ✅ Responsive design maintained

### Test 7: Edge Cases

**Test 7.1: Switch During Generation**
1. Start PRD generation with dev mode OFF
2. Turn dev mode ON mid-generation
3. Expected: No logs appear (mode set at start)

**Test 7.2: Multiple Generations**
1. Generate PRD with dev mode ON
2. Wait for completion
3. Generate another PRD with dev mode ON
4. Expected: Old logs cleared, new logs appear

**Test 7.3: Toggle Multiple Times**
1. Click toggle 10 times rapidly
2. Expected: Toggle handles state correctly, no errors

**Test 7.4: Long Business Problem**
1. Enter 500+ word business problem
2. Enable dev mode
3. Generate PRD
4. Expected: Logs still readable, no layout issues

---

## Browser Console Checks

Open browser console (F12) and verify:

1. ✅ No JavaScript errors
2. ✅ WebSocket connection established
3. ✅ Log messages: "Dev mode: ON" or "Dev mode: OFF"
4. ✅ WebSocket messages with type: 'log'
5. ✅ No CORS errors
6. ✅ No 404s or resource loading failures

---

## Backend Validation

Check server terminal output:

1. ✅ No Python exceptions
2. ✅ WebSocket connections logged
3. ✅ Request received with dev_mode flag
4. ✅ Agents created with correct verbose setting
5. ✅ No deprecation warnings

---

## Known Issues (Acceptable)

### Expected Behaviors:
- CrewAI may output some warnings to console (normal)
- First generation takes slightly longer (model loading)
- Very long logs may cause slight UI lag (acceptable)

### Not Issues:
- Emoji characters in terminal (cosmetic only)
- Unicode warnings (doesn't affect functionality)
- Verbose output from CrewAI (intended when dev mode ON)

---

## Success Criteria

**Feature is PASSING if:**
- ✅ Toggle switch works reliably
- ✅ Dev mode OFF = clean output, no logs
- ✅ Dev mode ON = detailed logs visible
- ✅ All three log types appear
- ✅ Timestamps are accurate
- ✅ Auto-scrolling works
- ✅ No JavaScript errors
- ✅ PRD still generates correctly
- ✅ Performance impact acceptable (<10% slower)
- ✅ UI remains responsive

---

## Quick Smoke Test (2 minutes)

**Minimal validation:**
1. Open http://localhost:8001
2. Toggle dev mode ON
3. Click example #1
4. Generate PRD
5. Verify logs appear
6. Wait for PRD completion
7. Download PDF to confirm end-to-end works

**If all 7 steps succeed → Feature is working! ✅**

---

## Troubleshooting

### No logs appearing when dev mode ON

**Check:**
```javascript
// Browser console:
console.log('devMode:', devMode);  // Should be true
```

**Solution:**
- Clear browser cache
- Hard refresh (Ctrl+Shift+R)
- Check WebSocket connection

### Logs not clearing between generations

**Check:**
```javascript
// In generatePRD():
if (devMode) {
    logsDiv.innerHTML = '';  // Should clear
}
```

**Solution:**
- Already implemented, may be browser cache

### Toggle not sending dev_mode to backend

**Check:**
```python
# Backend should receive:
problem.dev_mode  # True or False
```

**Solution:**
- Verify JSON payload in Network tab
- Check BusinessProblem model has dev_mode field

---

## Test Results

**Tested By:** _________________  
**Date:** _________________  
**Browser:** _________________  
**Results:** ☐ PASS  ☐ FAIL  

**Notes:**
_______________________________________
_______________________________________
_______________________________________

---

**Next Steps After Testing:**
1. ✅ Document any bugs found
2. ✅ Update CREWAI_ISSUES_LOG.md if needed
3. ✅ Consider additional enhancements
4. ✅ Get user feedback
5. ✅ Deploy to production if all tests pass

