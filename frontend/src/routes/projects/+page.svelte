<script lang="ts">
  import UpdateProject from "$lib/components/UpdateProject.svelte";
  import JoinProject from "$lib/components/JoinProject.svelte";
  import CreateProject from "$lib/components/CreateProject.svelte";
  import type { PageData } from "./$types";
import Collapse from "$lib/components/Collapse.svelte";
  let { data }: { data: PageData } = $props();
</script>

<div class="p-4 mx-auto space-y-4">
  <!-- <div > -->
  <section>
    <Collapse title="Your projects">
    <!-- <h2 class="text-xl font-semibold mb-4">Your projects</h2> -->
    <div class="overflow-x-auto">
    <table class="table w-full table-zebra">
      <thead>
        <tr>
          <th>Project Name</th>
          <th>Description</th>
          <th>Join Code</th>
        </tr>
      </thead>
      <tbody>
        {#each data.projects as project}
          <tr>
            <td>{project.name}</td>
            <td>{project.description}</td>
            <td
              ><a
                href={`/projects/?join_code=${project.join_code}`}
                data-sveltekit-noscroll>{project.join_code}</a
              ></td
            >
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</Collapse>
  </section>
  <section>
    <Collapse title="Create a project">
    <CreateProject />
    </Collapse>
  </section>
  <section>
    <Collapse title="Join a project">
    <JoinProject />
    </Collapse>
  </section>
  <section>
    <Collapse title="Update a project">
    <UpdateProject projects={data.projects} events={data.events} />
    </Collapse>
  </section>
</div>

<style>
  /* section {
    @apply p-6 rounded-lg shadow-sm border-accent border-2 border-dotted border-opacity-50;
  } */
  a {
    @apply underline rounded transition-colors duration-300 hover:bg-primary hover:text-primary-content p-1 underline-offset-2 decoration-accent;
  }
</style>
