import { defineCollection, z } from "astro:content";

const spikes = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    theme: z.string(),
    whyItMatters: z.string(),
    tags: z.array(z.string()),
    updatedAt: z.coerce.date(),
    sourceCount: z.number().int().nonnegative(),
    addedBy: z.string().optional(),
  }),
});

export const collections = { spikes };
