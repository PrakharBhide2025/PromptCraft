// const API = "/api/v1";
// const authHeader = () => ({
//   Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
//   "Content-Type": "application/json"
// });

// // export async function savePromptVersion(promptId, data) {
// //   const res = await fetch(`${API}/prompts/${promptId}/versions`, {
// //     method: "POST",
// //     headers: authHeader(),
// //     body: JSON.stringify(data)
// //   });
// //   return await res.json();
// // }
// export async function savePrompt(promptText, version = "v1") {
//   if (!promptText.trim()) {
//     alert("⚠️ Please enter a prompt before saving.");
//     return;
//   }

//   if (!version) {
//     alert("⚠️ Version name is required.");
//     return;
//   }

//   const savedPrompts = JSON.parse(localStorage.getItem("savedPrompts") || "{}");
//   const timestamp = new Date().toISOString();

//   // Save locally
//   savedPrompts[version] = {
//     prompt: promptText,
//     savedAt: timestamp
//   };
//   localStorage.setItem("savedPrompts", JSON.stringify(savedPrompts));
//   alert(`✅ Prompt saved locally as "${version}"`);

//   // Prepare backend payload
//   const payload = {
//     input_text: promptText,
//     purpose: "save_prompt",
//     name: version,
//     description: "Prompt from UI",
//     tags: [],
//     prompt_metadata: {}
//   };

//   console.log("🧪 Payload being sent:", payload);

//   try {
//     const response = await savePromptVersion(PROMPT_ID, payload);
//     console.log("✅ Saved to backend:", response);
//     alert(`✅ Prompt version "${version}" also saved to backend!`);
//   } catch (err) {
//     console.error("❌ Backend save failed", err);
//     alert("❌ Failed to save prompt to backend.");
//   }
// }

// export async function listPromptVersions(promptId) {
//   const res = await fetch(`${API}/prompts/${promptId}/versions`, {
//     headers: authHeader()
//   });
//   return await res.json();
// }

// export async function pushPromptToGitHub(payload) {
//   const res = await fetch(`${API}/github/push-version`, {
//     method: "POST",
//     headers: authHeader(),
//     body: JSON.stringify(payload)
//   });
//   return await res.json();
// }

// export async function connectGitHub() {
//   const res = await fetch(`${API}/github/login`, {
//     headers: authHeader()
//   });
//   const data = await res.json();
//   window.location.href = data.auth_url;
// }

// PromptService.js

// const API = "/api/v1";

// // Auth headers for all API requests
// const authHeader = () => ({
//   Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
//   "Content-Type": "application/json"
// });

// //
// // ✅ 1. Save a new version of a prompt (used by PromptEditor.js)
// //
// export async function savePromptVersion(promptId, data) {
//   const res = await fetch(`${API}/prompts/${promptId}/versions`, {
//     method: "POST",
//     headers: authHeader(),
//     body: JSON.stringify(data)
//   });

//   // Check for server errors
//   if (!res.ok) {
//     const errorDetail = await res.text();
//     console.error("❌ Backend error response:", errorDetail);
//     throw new Error("Failed to save prompt version.");
//   }

//   return await res.json();
// }

// //
// // ✅ 2. Save prompt locally AND send to backend (versioned)
// //
// export async function savePrompt(promptText, version = "v1") {
//   if (!promptText.trim()) {
//     alert("⚠️ Please enter a prompt before saving.");
//     return;
//   }

//   if (!version) {
//     alert("⚠️ Version name is required.");
//     return;
//   }

//   const savedPrompts = JSON.parse(localStorage.getItem("savedPrompts") || "{}");
//   const timestamp = new Date().toISOString();

//   // ✅ Save locally
//   savedPrompts[version] = {
//     prompt: promptText,
//     savedAt: timestamp
//   };
//   localStorage.setItem("savedPrompts", JSON.stringify(savedPrompts));
//   alert(`✅ Prompt saved locally as "${version}"`);

//   // ✅ Prepare payload for backend
//   const payload = {
//     input_text: promptText,
//     purpose: "save_prompt",
//     name: version,
//     content: promptText,
//     description: "Prompt from UI",
//     tags: [],
//     prompt_metadata: {}
//   };

//   console.log("🧪 Payload being sent:", payload);

//   try {
//     // Replace with actual prompt ID (from UI state or database)
//     const PROMPT_ID = localStorage.getItem("selectedPromptId") || "default-prompt-id";

//     const response = await savePromptVersion(PROMPT_ID, payload);
//     console.log("✅ Saved to backend:", response);
//     alert(`✅ Prompt version "${version}" also saved to backend!`);
//   } catch (err) {
//     console.error("❌ Backend save failed", err);
//     alert("❌ Failed to save prompt to backend.");
//   }
// }

// //
// // ✅ 3. List all versions of a prompt (by prompt ID)
// //
// export async function listPromptVersions(promptId) {
//   const res = await fetch(`${API}/prompts/${promptId}/versions`, {
//     headers: authHeader()
//   });
//   return await res.json();
// }

// //
// // ✅ 4. Push prompt version to GitHub
// //
// export async function pushPromptToGitHub(payload) {
//   const res = await fetch(`${API}/github/push-version`, {
//     method: "POST",
//     headers: authHeader(),
//     body: JSON.stringify(payload)
//   });
//   return await res.json();
// }

// //
// // ✅ 5. GitHub login / connect
// //
// export async function connectGitHub() {
//   const res = await fetch(`${API}/github/login`, {
//     headers: authHeader()
//   });
//   const data = await res.json();
//   window.location.href = data.auth_url;
// }

const API = "/api/v1";

// ✅ Auth headers for all API requests
const authHeader = () => ({
  Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
  "Content-Type": "application/json"
});

//
// ✅ 1. Create a new prompt (returns its ID)
//
export async function createPrompt(promptText, purpose = "generate_output", name = "User Prompt") {
  const payload = {
    input_text: promptText,
    purpose,
    name,
    description: "Prompt from UI",
    tags: [],
    prompt_metadata: {}
  };

  const res = await fetch(`${API}/prompts/`, {
    method: "POST",
    headers: authHeader(),
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    const errorDetail = await res.text();
    console.error("❌ Prompt creation failed:", errorDetail);
    throw new Error("Failed to create prompt.");
  }

  const data = await res.json();
  const promptId = data.id;

  // ✅ Save prompt ID to localStorage for future reference
  localStorage.setItem("selectedPromptId", promptId);
  console.log("✅ Prompt created with ID:", promptId);

  return promptId;
}

//
// ✅ 2. Save a new version of a prompt
//
export async function savePromptVersion(promptId, data) {
  const res = await fetch(`${API}/prompts/${promptId}/versions`, {
    method: "POST",
    headers: authHeader(),
    body: JSON.stringify(data)
  });

  if (!res.ok) {
    const errorDetail = await res.text();
    console.error("❌ Backend error response:", errorDetail);
    throw new Error("Failed to save prompt version.");
  }

  return await res.json();
}

//
// ✅ 3. Save prompt locally and optionally sync with backend
//
export async function savePrompt(promptText, version = "v1") {
  if (!promptText.trim()) {
    alert(" Please enter a prompt before saving.");
    return;
  }

  if (!version) {
    alert(" Version name is required.");
    return;
  }

  const savedPrompts = JSON.parse(localStorage.getItem("savedPrompts") || "{}");
  const timestamp = new Date().toISOString();

  // Save locally
  savedPrompts[version] = {
    prompt: promptText,
    savedAt: timestamp
  };
  localStorage.setItem("savedPrompts", JSON.stringify(savedPrompts));
  alert(` Prompt saved locally as "${version}"`);

  // Create prompt if not already saved
  let promptId = localStorage.getItem("selectedPromptId");
  if (!promptId || promptId === "default-prompt-id") {
    promptId = await createPrompt(promptText); // ⬅️ use createPrompt to get ID
  }

  const payload = {
    input_text: promptText,
    purpose: "save_prompt",
    name: version,
    content: promptText,
    description: "Prompt version from UI",
    tags: [],
    prompt_metadata: {}
  };

  try {
    const response = await savePromptVersion(promptId, payload);
    console.log(" Saved to backend:", response);
    alert(` Prompt version "${version}" also saved to backend!`);
  } catch (err) {
    console.error("  Backend save failed", err);
    alert(" Failed to save prompt to backend.");
  }
}

//
// ✅ 4. List all versions of a prompt (by prompt ID)
//
export async function listPromptVersions(promptId) {
  const res = await fetch(`${API}/prompts/${promptId}/versions`, {
    headers: authHeader()
  });
  return await res.json();
}

//
// ✅ 5. Push prompt version to GitHub
//
export async function pushPromptToGitHub(payload) {
  const res = await fetch(`${API}/github/push-version`, {
    method: "POST",
    headers: authHeader(),
    body: JSON.stringify(payload)
  });
  return await res.json();
}

//
// ✅ 6. GitHub login / connect
//
export async function connectGitHub() {
  const res = await fetch(`${API}/github/login`, {
    headers: authHeader()
  });
  const data = await res.json();
  window.location.href = data.auth_url;
}
