# QUICK FIX: Power Automate base64ToBinary Error

## The Problem
```
InvalidTemplate. Unable to process template language expressions in action 'Create_file'
The template language function 'base64ToBinary' expects its parameter to be a string.
The provided value is of type 'Null'.
```

## The Solution: Fix File Content Expression

### Step-by-Step Fix:

1. **Open your Power Automate flow**
   - Go to https://make.powerautomate.com
   - Find: "Upload API Report to SharePoint"
   - Click **Edit**

2. **Click on the "Create file" SharePoint action**

3. **Fix the File Content field:**
   - Click in the **File Content** field
   - You'll see tabs: "Dynamic content" and "Expression"
   - Click the **"Expression"** tab (important!)
   - Clear any existing content
   - Type EXACTLY this (copy-paste to be safe):
   ```
   base64ToBinary(triggerBody()['fileContent'])
   ```
   - **IMPORTANT:** NO question mark before the brackets!
   - Click **OK**

4. **Also check File Name field:**
   - Should be: `triggerBody()['filename']` (NO question mark)
   - Or use Dynamic content and select "filename"

5. **Save the flow**
   - Click **Save** in the top right

6. **Test again**
   - Run: `python test_flow_simple.py`
   - Should now see HTTP 200 instead of 500

---

## Why This Happens

The `?` in `triggerBody()?['fileContent']` makes the value **optional**.
- If the trigger body exists → returns the value
- If anything is missing → returns **Null**

When Power Automate evaluates this in the SharePoint action, it's treating it as Null instead of accessing the actual field.

**Removing the `?`** forces it to directly access the field value.

---

## Visual Guide

**WRONG (causes Null error):**
```
File Content: @{base64ToBinary(triggerBody()?['fileContent'])}
                                           ↑
                                    Remove this!
```

**CORRECT:**
```
File Content: @{base64ToBinary(triggerBody()['fileContent'])}
                                           ↑
                                      No ? here
```

---

## Alternative: Use Dynamic Content

Instead of Expression, you can also:
1. In File Content field, click "Dynamic content" tab
2. Under "When a HTTP request is received" section
3. Look for "fileContent" and click it
4. Then wrap it in base64ToBinary by switching to Expression tab
5. You should see: `base64ToBinary(triggerOutputs()?['body']?['fileContent'])`

But the simplest is: `base64ToBinary(triggerBody()['fileContent'])`
