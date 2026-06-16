# Admin Prediction Editing Feature

## Overview

Admins can now create, edit, and delete user predictions even after matches are finished. This is useful for:
- Correcting user mistakes
- Adding predictions for users who missed the deadline
- Managing prediction data
- Testing and debugging

## New Admin Endpoints

### 1. Update Prediction (PUT)
**Endpoint**: `/api/admin/predictions/<prediction_id>`  
**Method**: PUT  
**Admin Only**: Yes  
**Works After Match Finished**: ✅ Yes

Update any user's prediction, even after the match is finished. Points are automatically recalculated.

**Request Body:**
```json
{
  "predicted_home_score": 2,
  "predicted_away_score": 1
}
```

**Response:**
```json
{
  "message": "Prediction updated successfully",
  "prediction": {
    "id": 123,
    "user": "john_doe",
    "match": "Brazil vs Argentina",
    "predicted_home_score": 2,
    "predicted_away_score": 1,
    "points_earned": 3
  }
}
```

### 2. Delete Prediction (DELETE)
**Endpoint**: `/api/admin/predictions/<prediction_id>`  
**Method**: DELETE  
**Admin Only**: Yes

Delete any user's prediction.

**Response:**
```json
{
  "message": "Prediction deleted successfully",
  "deleted": {
    "user": "john_doe",
    "match": "Brazil vs Argentina"
  }
}
```

### 3. Create Prediction (POST)
**Endpoint**: `/api/admin/predictions/create`  
**Method**: POST  
**Admin Only**: Yes  
**Works After Match Finished**: ✅ Yes

Create a prediction for any user, even after the match is finished. Points are automatically calculated if the match is already finished.

**Request Body:**
```json
{
  "user_id": 5,
  "match_id": 10,
  "predicted_home_score": 2,
  "predicted_away_score": 1
}
```

**Response:**
```json
{
  "message": "Prediction created successfully",
  "prediction": {
    "id": 124,
    "user": "john_doe",
    "match": "Brazil vs Argentina",
    "predicted_home_score": 2,
    "predicted_away_score": 1,
    "points_earned": 3
  }
}
```

## Usage Examples

### Using curl

**1. Update a prediction:**
```bash
curl -X PUT https://your-app.onrender.com/api/admin/predictions/123 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"predicted_home_score": 2, "predicted_away_score": 1}'
```

**2. Delete a prediction:**
```bash
curl -X DELETE https://your-app.onrender.com/api/admin/predictions/123 \
  -b cookies.txt
```

**3. Create a prediction:**
```bash
curl -X POST https://your-app.onrender.com/api/admin/predictions/create \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "user_id": 5,
    "match_id": 10,
    "predicted_home_score": 2,
    "predicted_away_score": 1
  }'
```

### Using JavaScript (Browser Console)

**1. Update a prediction:**
```javascript
fetch('/api/admin/predictions/123', {
  method: 'PUT',
  credentials: 'include',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    predicted_home_score: 2,
    predicted_away_score: 1
  })
})
.then(r => r.json())
.then(data => console.log(data));
```

**2. Delete a prediction:**
```javascript
fetch('/api/admin/predictions/123', {
  method: 'DELETE',
  credentials: 'include'
})
.then(r => r.json())
.then(data => console.log(data));
```

**3. Create a prediction:**
```javascript
fetch('/api/admin/predictions/create', {
  method: 'POST',
  credentials: 'include',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user_id: 5,
    match_id: 10,
    predicted_home_score: 2,
    predicted_away_score: 1
  })
})
.then(r => r.json())
.then(data => console.log(data));
```

## How to Get IDs

### Get Prediction ID
Use the existing endpoint to see all predictions:
```
GET /api/admin/predictions
```

Or by match:
```
GET /api/admin/predictions/by-match
```

### Get User ID
Use the users endpoint:
```
GET /api/admin/users
```

### Get Match ID
Use the matches endpoint:
```
GET /api/matches
```

## Key Features

✅ **Works After Match Finished** - Unlike regular predictions, admins can edit even after matches end  
✅ **Auto-Recalculates Points** - Points are automatically updated when editing finished match predictions  
✅ **Full CRUD Operations** - Create, Read, Update, Delete  
✅ **Safe & Validated** - Checks for valid users, matches, and data  
✅ **Admin Only** - Requires admin authentication  

## Use Cases

### 1. Correct User Mistakes
User accidentally entered wrong scores? Admin can fix it:
```javascript
// Update prediction ID 123 to correct scores
fetch('/api/admin/predictions/123', {
  method: 'PUT',
  credentials: 'include',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    predicted_home_score: 3,  // Corrected
    predicted_away_score: 2   // Corrected
  })
});
```

### 2. Add Late Predictions
User missed the deadline? Admin can add their prediction:
```javascript
// Create prediction for user 5, match 10
fetch('/api/admin/predictions/create', {
  method: 'POST',
  credentials: 'include',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user_id: 5,
    match_id: 10,
    predicted_home_score: 2,
    predicted_away_score: 1
  })
});
```

### 3. Remove Invalid Predictions
Found a duplicate or invalid prediction? Admin can delete it:
```javascript
// Delete prediction ID 123
fetch('/api/admin/predictions/123', {
  method: 'DELETE',
  credentials: 'include'
});
```

## Important Notes

- ⚠️ **Admin access required** - Must be logged in as admin
- ⚠️ **Points auto-update** - When editing finished match predictions, points recalculate automatically
- ⚠️ **No duplicate check on update** - Can update any existing prediction
- ⚠️ **Duplicate check on create** - Cannot create if prediction already exists (use PUT to update)
- ✅ **Audit trail** - All changes are logged in the database

## Troubleshooting

### "Admin access required"
- Make sure you're logged in as an admin user
- Check your session cookie is being sent

### "Prediction already exists"
- When creating, if prediction exists, use PUT to update instead
- Get the prediction ID from `/api/admin/predictions`

### "User not found" or "Match not found"
- Verify the user_id and match_id exist
- Use `/api/admin/users` and `/api/matches` to get valid IDs

## Security

- All endpoints require admin authentication
- Regular users cannot access these endpoints
- Changes are logged with timestamps
- Points are recalculated automatically to prevent cheating

---

## Summary

Admins now have full control over predictions:
- ✅ Edit predictions after matches finish
- ✅ Create predictions for any user
- ✅ Delete invalid predictions
- ✅ Points automatically recalculate

Perfect for managing your World Cup predictor!

---
*Last updated: 2026-06-16*