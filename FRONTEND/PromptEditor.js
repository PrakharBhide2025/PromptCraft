// // PromptEditor.js

// // Store prompt in localStorage with optional versioning
// import { savePromptVersion } from "./PromptService.js";

// export async function savePrompt(promptText, version = "v1") {
//   const savedPrompts = JSON.parse(localStorage.getItem("savedPrompts") || "{}");
//   const timestamp = new Date().toISOString();

//   savedPrompts[version] = {
//     prompt: promptText,
//     savedAt: timestamp
//   };

//   localStorage.setItem("savedPrompts", JSON.stringify(savedPrompts));
//   alert(`Prompt saved locally as ${version}`);

//   // ✅ Send to backend
//   try {
//     const payload = {
//       input_text: promptText,
//       purpose: "save_prompt",    
//       name: version,                 //
//       description: "Prompt from UI",
//       tags: [],
//       prompt_metadata: {}
//     };

//     // NOTE: Replace `yourPromptIdHere` with the actual prompt ID if you use one
//     const response = await savePromptVersion("yourPromptIdHere", payload);
//     console.log("Saved to backend:", response);
//   } catch (err) {
//     console.error("Backend save failed", err);
//   }
// }

// // Load a saved prompt version into the editor
// export function loadPrompt(version = "v1") {
//   const savedPrompts = JSON.parse(localStorage.getItem("savedPrompts") || "{}");

//   if (!savedPrompts[version]) {
//     alert(`No prompt found for version ${version}`);
//     return;
//   }

//   const promptText = savedPrompts[version].prompt;
//   const editor = document.getElementById("promptEditor");
//   if (editor) {
//     editor.value = promptText;
//   }

//   return promptText;
// }

// // Show list of all saved versions in console or UI
// export function listPromptVersions() {
//   const savedPrompts = JSON.parse(localStorage.getItem("savedPrompts") || "{}");
//   return Object.keys(savedPrompts);
// }

// // Example: Wire up buttons after DOM loads
// window.addEventListener("DOMContentLoaded", () => {
//   const saveBtn = document.getElementById("savePromptBtn");
//   const loadBtn = document.getElementById("loadPromptBtn");

//   if (saveBtn) {
//     saveBtn.addEventListener("click", () => {
//       const promptText = document.getElementById("promptEditor").value;
//       const version = prompt("Enter version name:", "v1");
//       if (promptText && version) {
//         savePrompt(promptText, version);
//       }
//     });
//   }

//   if (loadBtn) {
//     loadBtn.addEventListener("click", () => {
//       const version = prompt("Enter version name to load:", "v1");
//       if (version) {
//         loadPrompt(version);
//       }
//     });
//   }
// });

// PromptEditor.js

// import { savePromptVersion } from "./PromptService.js";

// // ✅ Load a real prompt ID from localStorage or user selection
// const PROMPT_ID = localStorage.getItem("selectedPromptId");  // must be set during prompt creation

// export async function savePrompt(promptText, version = "v1") {
//   const savedPrompts = JSON.parse(localStorage.getItem("savedPrompts") || "{}");
//   const timestamp = new Date().toISOString();

//   // ✅ Save locally
//   savedPrompts[version] = {
//     prompt: promptText,
//     savedAt: timestamp
//   };
//   localStorage.setItem("savedPrompts", JSON.stringify(savedPrompts));
//   alert(`✅ Prompt saved locally as "${version}"`);

//   // ✅ Save to backend
//   try {
//     if (!PROMPT_ID) {
//       alert("❌ No Prompt ID found. Please select or create a prompt first.");
//       return;
//     }

//     const payload = {
//       input_text: promptText,
//       purpose: "code-generation",  // or "save_prompt" if preferred
//       name: version,
//       content: promptText,
//       description: "Prompt submitted from frontend",
//       tags: [],
//       prompt_metadata: {}
//     };

//     const response = await savePromptVersion(PROMPT_ID, payload);
//     console.log("✅ Saved to backend:", response);
//     alert(`✅ Prompt version "${version}" also saved to backend!`);
//   } catch (err) {
//     console.error("❌ Backend save failed", err);
//     alert("❌ Failed to save prompt to backend.");
//   }
// }

// export function loadPrompt(version = "v1") {
//   const savedPrompts = JSON.parse(localStorage.getItem("savedPrompts") || "{}");

//   if (!savedPrompts[version]) {
//     alert(`⚠️ No prompt found for version "${version}"`);
//     return;
//   }

//   const promptText = savedPrompts[version].prompt;
//   const editor = document.getElementById("promptEditor");
//   if (editor) {
//     editor.value = promptText;
//   }

//   return promptText;
// }

// export function listPromptVersions() {
//   const savedPrompts = JSON.parse(localStorage.getItem("savedPrompts") || "{}");
//   return Object.keys(savedPrompts);
// }

// window.addEventListener("DOMContentLoaded", () => {
//   const saveBtn = document.getElementById("savePromptBtn");
//   const loadBtn = document.getElementById("loadPromptBtn");

//   if (saveBtn) {
//     saveBtn.addEventListener("click", async () => {
//       const promptText = document.getElementById("promptEditor").value;
//       const version = prompt("Enter version name:", "v1");
//       if (promptText && version) {
//         await savePrompt(promptText, version);
//       }
//     });
//   }

//   if (loadBtn) {
//     loadBtn.addEventListener("click", () => {
//       const version = prompt("Enter version name to load:", "v1");
//       if (version) {
//         loadPrompt(version);
//       }
//     });
//   }
// });

import { savePromptVersion } from "./PromptService.js";

export async function savePrompt(promptText, version = "v1") {
  const savedPrompts = JSON.parse(localStorage.getItem("savedPrompts") || "{}");
  const timestamp = new Date().toISOString();

  // ✅ Save locally
  savedPrompts[version] = {
    prompt: promptText,
    savedAt: timestamp
  };
  localStorage.setItem("savedPrompts", JSON.stringify(savedPrompts));
  alert(` Prompt saved locally as "${version}"`);

  // ✅ Save to backend
  try {
    const promptId = localStorage.getItem("selectedPromptId");  // ✅ Read dynamically

    if (!promptId) {
  alert(" No Prompt ID found. Please create a prompt on the Get Started page first.");
  window.location.href = "getstarted.html"; 
  return;
}

    const payload = {
      input_text: promptText,
      purpose: "code-generation",  // or "save_prompt"
      name: version,
      content: promptText,
      description: "Prompt submitted from frontend",
      tags: [],
      prompt_metadata: {}
    };

    const response = await savePromptVersion(promptId, payload);
    console.log(" Saved to backend:", response);
    alert(` Prompt version "${version}" also saved to backend!`);
  } catch (err) {
    console.error(" Backend save failed", err);
    alert("  Failed to save prompt to backend.");
  }
}

export function loadPrompt(version = "v1") {
  const savedPrompts = JSON.parse(localStorage.getItem("savedPrompts") || "{}");

  if (!savedPrompts[version]) {
    alert(` No prompt found for version "${version}"`);
    return;
  }

  const promptText = savedPrompts[version].prompt;
  const editor = document.getElementById("promptEditor");
  if (editor) {
    editor.value = promptText;
  }

  return promptText;
}

export function listPromptVersions() {
  const savedPrompts = JSON.parse(localStorage.getItem("savedPrompts") || "{}");
  return Object.keys(savedPrompts);
}

window.addEventListener("DOMContentLoaded", () => {
  const saveBtn = document.getElementById("savePromptBtn");
  const loadBtn = document.getElementById("loadPromptBtn");

  if (saveBtn) {
    saveBtn.addEventListener("click", async () => {
      const promptText = document.getElementById("promptEditor").value;
      const version = prompt("Enter version name:", "v1");
      if (promptText && version) {
        await savePrompt(promptText, version);
      }
    });
  }

  if (loadBtn) {
    loadBtn.addEventListener("click", () => {
      const version = prompt("Enter version name to load:", "v1");
      if (version) {
        loadPrompt(version);
      }
    });
  }
});

