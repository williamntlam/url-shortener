
## ✅ Phase 2: URL Shortening Core

- Create a `Pydantic` model to validate incoming URL requests (e.g., `original_url: str`).
- Generate a short code using `base62`, `shortuuid`, or custom logic.
- Store the original URL and short code in MongoDB via a service function.
- Return the shortened URL as part of the API response.

---

## ✅ Phase 3: Redirection + Caching

- Create a `GET /{short_code}` route to handle redirection.
- Implement a **cache-aside pattern**:
- First, check Redis for the `short_code`.
- If not cached, fetch from MongoDB.
- Store it in Redis for future use.
- Redirect the client to the original URL using a 302/301 response.

---

## ✅ Phase 4: Analytics Logging

- Add a background task (using FastAPI's `BackgroundTasks`) to log:
- IP address
- Timestamp
- Referrer (from headers)
- User-Agent (from headers)
- Store analytics in a separate MongoDB collection (e.g., `click_logs`), or enqueue them in Redis for async processing with a worker.

---

## ✅ Phase 5: Rate Limiting

- Start with a package like `slowapi` to apply rate limits to the `/shorten` endpoint.
- Later, replace with a **custom-built rate limiter** using:
- Redis
- IP-based tracking
- A fixed window or token bucket algorithm for per-user limits

---

## ✅ Phase 6: Svelte Frontend

- Set up a Svelte or SvelteKit frontend project.
- Create a form that:
- Accepts a long URL input
- Submits it to the backend `/shorten` route
- Displays the returned short URL
- (Optional) Add a dashboard for:
- Showing total clicks
- Viewing analytics per short URL

---

## ✅ Phase 7: Production Readiness

- Add structured logging and centralized error handling.
- Secure endpoints by:
- Enabling CORS
- Validating and sanitizing input
- Whitelisting safe domains if needed
- Deploy the application:
- Backend: **Render**, **Railway**, **Fly.io**, or **Heroku**
- Frontend: **Vercel**, **Netlify**, or **Cloudflare Pages**
- Use environment variables to toggle between dev/staging/production URLs.

---

## 🚀 Optional Extensions

- ✅ User authentication for managing personal short links
- ✅ Custom aliases (e.g., `/william`)
- ✅ Link expiration or one-time use URLs
- ✅ QR code generation
- ✅ Geolocation heatmaps or timezone-aware click analysis
- ✅ Admin panel for banning spammy links or flagging suspicious activity

---

## 📂 Example Monorepo Structure

