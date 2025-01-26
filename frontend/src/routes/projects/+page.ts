// https://svelte.dev/docs/kit/load#Layout-data
import { error, redirect } from "@sveltejs/kit";
import type { PageLoad } from "./$types";
import { user } from "$lib/user.svelte";
import { client, EventsService, ProjectsService } from "$lib/client/sdk.gen";
import type { Event, OwnerProject, UserEvents } from "$lib/client/types.gen";

export const load: PageLoad = async ({ params, fetch, depends }) => {
  // depends("events:events")
  // depends("projects:mine")

  client.setConfig({ fetch });
  if (!user.isAuthenticated) {
    throw error(401, "Unauthorized, try logging in first");
  }

  let events: Array<Event> = [];
  let projects: Array<OwnerProject> = [];
  
  try {
      const { data } = await EventsService.getAttendingEventsEventsGet({
        throwOnError: true,
      });
      events = data.attending_events
    } catch (err) {
      console.error(err);
      throw error(500, "Failed to load events");
    }

  try {
    const { data } = await ProjectsService.getProjectsProjectsMineGet({
      throwOnError: true,
    });
    projects = data;
  } catch (err) {
    console.error(err);
    throw error(500, "Failed to load projects");
  }

  return {
    events,
    projects
  }
};
