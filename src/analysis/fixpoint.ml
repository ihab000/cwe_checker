open Bap.Std
open Core_kernel


module type ProblemSig = sig
  type t
  module Node: Regular.Std.Opaque.S
  module EdgeLabel: Core_kernel.T
  module BapGraph: Graphlib.Std.Graph with type node = Node.t and type Edge.label = EdgeLabel.t


  val merge: t -> t -> t
  val equal: t -> t -> Bool.t
  val update_edge: t -> BapGraph.Edge.t -> t Option.t
end

module type FixpointSig = sig
  type t
  type node_label
  type edge_label
  type value_type

  module BapGraph: Graphlib.Std.Graph with type node = node_label and type Edge.label = edge_label

  val empty: ?default:value_type -> BapGraph.t -> t

  val get_node_value: t -> node_label -> value_type Option.t

  val set_node_value: t -> node_label -> value_type -> t

  val get_worklist: t -> node_label List.t

  val compute: ?max_steps:Int.t -> t -> t
end

module Fixpoint (FP : ProblemSig) : FixpointSig
  with type node_label = FP.Node.t and type edge_label = FP.EdgeLabel.t and type value_type = FP.t
= struct

  module BapGraph = FP.BapGraph
  module OcamlGraph = Graphlib.Std.Graphlib.To_ocamlgraph(BapGraph)
  module TopologicalGraph = Graph.Topological.Make(OcamlGraph)

  type node_label = FP.Node.t
  type edge_label = FP.EdgeLabel.t
  type value_type = FP.t

  type t = {
    graph: BapGraph.t;
    nodes_topological_order: FP.Node.t Array.t;
    node_to_index_map: (FP.Node.t, Int.t, FP.Node.comparator_witness) Map.t;
    node_values: (FP.Node.t, FP.t, FP.Node.comparator_witness) Map.t;
    default_value: FP.t Option.t;
    worklist: Int.Set.t;
  }

  let empty ?default (graph: BapGraph.t) : t =
    let nodes_list = TopologicalGraph.fold (fun node node_list -> node :: node_list) graph [] in
    let nodes_topological_order = Array.of_list (List.rev nodes_list) in (* TODO: test out correct ordering here! *)
    let node_to_index_map = Array.foldi nodes_topological_order ~init:FP.Node.Map.empty ~f:(fun index map elem -> Map.set map ~key:elem ~data:index) in
    let worklist = match default with
      | None -> Int.Set.empty
      | Some _ -> Int.Set.of_array (Array.mapi nodes_topological_order ~f:(fun index _elem -> index)) in
    { graph = graph;
      nodes_topological_order = nodes_topological_order;
      node_to_index_map = node_to_index_map;
      node_values = Map.empty (module FP.Node);
      default_value = default;
      worklist = worklist;
    }

  let get_node_value (solution : t) (node : FP.Node.t) : FP.t Option.t =
      match Map.find solution.node_values node with
      | Some value -> Some value
      | None -> solution.default_value

  let set_node_value (solution : t) (node : FP.Node.t) (elem : FP.t) : t =
    let node_index = Map.find_exn solution.node_to_index_map node in
    { solution with node_values = Map.set solution.node_values ~key:node ~data:elem;
                    worklist = Set.add solution.worklist node_index }

  let get_worklist (solution : t) : FP.Node.t List.t =
    Set.fold solution.worklist ~init:[] ~f:(fun node_list node_index -> solution.nodes_topological_order.(node_index) :: node_list)

  let update_edge (solution : t) (edge : BapGraph.Edge.t) : t =
    let value_src_option = get_node_value solution (BapGraph.Edge.src edge) in
    match value_src_option with
    | None -> solution
    | Some value_src ->
        let target_node = BapGraph.Edge.dst edge in
        let new_value_option = FP.update_edge value_src edge in
        let old_value_option = get_node_value solution target_node in
        match (old_value_option, new_value_option) with
        | (_, None) ->
            solution
        | (None, Some new_value) ->
            set_node_value solution target_node new_value
        | (Some old_value, Some new_value) ->
            if FP.equal old_value new_value then
              solution
            else
              let merged_value = FP.merge old_value new_value in
              set_node_value solution target_node merged_value

  let update_node (solution : t) (node_index : Int.t) : t =
    let solution = { solution with worklist = Set.remove solution.worklist node_index} in
    let output_edges = BapGraph.Node.outputs solution.nodes_topological_order.(node_index) solution.graph in
    Seq.fold output_edges ~init:solution ~f:(fun solution edge ->
      update_edge solution edge
    )


  let compute ?max_steps (solution : t) : t =
    let solution = ref solution in
    let () = match max_steps with
    | None ->
        while false = Set.is_empty !solution.worklist do
          let current_node_index = Set.min_elt_exn !solution.worklist in
          solution := update_node !solution current_node_index
        done
    | Some max ->
        let steps = Array.init (Array.length !solution.nodes_topological_order) ~f:(fun _i -> 0) in
        while false = Set.is_empty !solution.worklist do
          let current_node_index = Set.min_elt_exn !solution.worklist in
          if steps.(current_node_index) >= max then
            solution := { !solution with worklist = Set.remove !solution.worklist current_node_index}
          else
            steps.(current_node_index) <- steps.(current_node_index) + 1;
            solution := update_node !solution current_node_index
        done;
        (* we add all nodes that reached max_steps back into the worklist *)
        let max_steps_reached = Array.filter_mapi steps ~f:(fun index steps ->
          if steps >= max then
            Some index
          else
            None ) in
        let max_steps_worklist = Array.fold max_steps_reached ~init:Int.Set.empty ~f:(fun worklist index -> Int.Set.add worklist index) in
        solution := { !solution with worklist = max_steps_worklist}
    in
    !solution

end