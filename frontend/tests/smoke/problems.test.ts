// import { describe, expect, test } from "vitest";
// import { apiClient } from "@/shared/api/client";
//
// describe("problems api", () => {
//   test("prints public problems response", async () => {
//     const { data, error, response } = await apiClient.GET(
//       "/api/v1/subjects/{subject_slug}/problems/",
//       {
//         params: {
//           path: {
//             subject_slug: "chemistry",
//           },
//           query: {
//             offset: 0,
//             limit: 10,
//           },
//         },
//       },
//     );
//
//     console.log("STATUS:", response.status);
//     console.log("DATA:", JSON.stringify(data, null, 2));
//     console.log("ERROR:", JSON.stringify(error, null, 2));
//
//     expect(response.status).toBe(200);
//   });
// });
