<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import "./style.css";
import {API_BASE_URL} from '../src/config';
const file = ref(null);
const files = ref([]);
const fileInput = ref(null);

// handle file input
const handleFileChange = (e) => {
  file.value = e.target.files[0];
};

// upload file
const uploadFile = async () => {
  if (!file.value) return;

  const formData = new FormData();
  formData.append("file", file.value);

  await axios.post(`${API_BASE_URL}/upload`, formData);

  file.value = null;
  if (fileInput.value) fileInput.value.value = "";

  getFiles();
};

// get files
const getFiles = async () => {
  const res = await axios.get(`${API_BASE_URL}/files`);
  files.value = res.data;
};

// delete file
const deleteFile = async (id) => {
  await axios.delete(`${API_BASE_URL}/files/${id}`);
  getFiles();
};

// =====================
// 📝 TODO STATE
// =====================
const task = ref("");
const tasks = ref([]);

// ✅ EDIT STATE (FIXED)
const editingId = ref(null);
const editingText = ref("");

// add task
const addTask = async () => {
  if (!task.value) return;

  await axios.post(`${API_BASE_URL}/todos`, {
    title: task.value,
  });

  task.value = "";
  getTasks();
};

// start edit
const startEdit = (t) => {
  editingId.value = t.id;
  editingText.value = t.title;
};

// cancel edit
const cancelEdit = () => {
  editingId.value = null;
  editingText.value = "";
};

// update task
const updateTask = async (id) => {
  await axios.put(`${API_BASE_URL}/todos/${id}`, {
    title: editingText.value,
  });

  editingId.value = null;
  editingText.value = "";
  getTasks();
};

// get tasks
const getTasks = async () => {
  const res = await axios.get(`${API_BASE_URL}/todos`);
  tasks.value = res.data;
};

// delete task
const deleteTask = async (id) => {
  await axios.delete(`${API_BASE_URL}/todos/${id}`);
  getTasks();
};

// load data
onMounted(() => {
  getTasks();
  getFiles();
});
</script>

<template>
  <div class="flex min-h-screen bg-gray-900 text-white">

    <!-- Sidebar -->
    <aside class="w-60 bg-gray-800 p-5 flex flex-col">
      <h2 class="text-xl font-bold mb-6">📁 FileVault</h2>

      <button class="bg-purple-600 p-2 rounded mb-3">Dashboard</button>
      <button class="p-2 rounded hover:bg-gray-700">Uploads</button>

      <div class="mt-auto text-sm text-gray-400">
        Storage Used
      </div>
    </aside>

    <!-- Main -->
    <div class="flex-1 p-6">

      <!-- Header -->
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold">Dashboard</h1>

        <button
          @click="uploadFile"
          class="bg-green-500 hover:bg-green-600 transition px-4 py-2 rounded"
        >
          Upload
        </button>
      </div>

      <!-- Upload Box -->
      <div class="bg-gray-800 p-6 rounded-lg mb-6">
        <input
          type="file"
          ref="fileInput"
          @change="handleFileChange"
          class="mb-2"
        />

        <p v-if="file" class="text-sm text-gray-400">
          Selected: {{ file.name }}
        </p>
      </div>

      <!-- Files Table -->
      <div class="bg-gray-800 rounded-lg overflow-hidden">
        <table class="w-full text-left">
          <thead class="bg-gray-700 text-sm">
            <tr>
              <th class="p-3">File</th>
              <th class="p-3">Action</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="f in files"
              :key="f.id"
              class="border-t border-gray-700"
            >
              <td class="p-3">
                <a
                  :href="`${API_BASE_URL}/uploads/${f.filename}`"
                  target="_blank"
                  class="text-blue-400 underline"
                >
                  {{ f.filename }}
                </a>
              </td>

              <td class="p-3">
                <button
                  @click="deleteFile(f.id)"
                  class="text-red-400 hover:text-red-600"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="files.length === 0" class="p-4 text-gray-400">
          No files uploaded yet
        </div>
      </div>

      <!-- Tasks -->
      <div class="bg-gray-800 p-6 rounded-lg mt-6">
        <h2 class="text-lg mb-3">Tasks</h2>

        <div class="flex gap-2 mb-4">
          <input
            v-model="task"
            class="p-2 rounded text-black w-full"
            placeholder="Enter task"
          />
          <button
            @click="addTask"
            class="bg-blue-500 hover:bg-blue-600 px-4 rounded"
          >
            Add
          </button>
        </div>

        <ul>
          <li
            v-for="t in tasks"
            :key="t.id"
            class="flex justify-between items-center mb-2"
          >
            <!-- EDIT MODE -->
            <div v-if="editingId === t.id" class="flex gap-2 w-full">
              <input
                v-model="editingText"
                class="p-2 rounded text-black w-full"
              />

              <button
                @click="updateTask(t.id)"
                class="bg-green-500 px-2 rounded"
              >
                Save
              </button>

              <button
                @click="cancelEdit"
                class="bg-gray-500 px-2 rounded"
              >
                Cancel
              </button>
            </div>

            <!-- NORMAL MODE -->
            <div v-else class="flex justify-between w-full">
              <span>{{ t.title }}</span>

              <div class="flex gap-2">
                <button
                  @click="startEdit(t)"
                  class="text-yellow-400"
                >
                  Edit
                </button>

                <button
                  @click="deleteTask(t.id)"
                  class="text-red-400"
                >
                  Delect
                </button>
              </div>
            </div>
          </li>
        </ul>
      </div>

    </div>
  </div>
</template>