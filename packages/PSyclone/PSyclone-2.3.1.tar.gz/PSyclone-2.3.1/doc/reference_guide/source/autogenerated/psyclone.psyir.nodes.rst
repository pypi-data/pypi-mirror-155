========================
``psyclone.psyir.nodes``
========================

.. automodule:: psyclone.psyir.nodes

   .. contents::
      :local:


Submodules
==========

.. toctree::

   psyclone.psyir.nodes.acc_directives
   psyclone.psyir.nodes.array_member
   psyclone.psyir.nodes.array_mixin
   psyclone.psyir.nodes.array_of_structures_member
   psyclone.psyir.nodes.array_of_structures_mixin
   psyclone.psyir.nodes.array_of_structures_reference
   psyclone.psyir.nodes.array_reference
   psyclone.psyir.nodes.assignment
   psyclone.psyir.nodes.call
   psyclone.psyir.nodes.clause
   psyclone.psyir.nodes.codeblock
   psyclone.psyir.nodes.commentable_mixin
   psyclone.psyir.nodes.container
   psyclone.psyir.nodes.datanode
   psyclone.psyir.nodes.directive
   psyclone.psyir.nodes.extract_node
   psyclone.psyir.nodes.file_container
   psyclone.psyir.nodes.ifblock
   psyclone.psyir.nodes.kernel_schedule
   psyclone.psyir.nodes.literal
   psyclone.psyir.nodes.loop
   psyclone.psyir.nodes.member
   psyclone.psyir.nodes.nan_test_node
   psyclone.psyir.nodes.node
   psyclone.psyir.nodes.omp_clauses
   psyclone.psyir.nodes.omp_directives
   psyclone.psyir.nodes.operation
   psyclone.psyir.nodes.profile_node
   psyclone.psyir.nodes.psy_data_node
   psyclone.psyir.nodes.ranges
   psyclone.psyir.nodes.read_only_verify_node
   psyclone.psyir.nodes.reference
   psyclone.psyir.nodes.return_stmt
   psyclone.psyir.nodes.routine
   psyclone.psyir.nodes.schedule
   psyclone.psyir.nodes.scoping_node
   psyclone.psyir.nodes.statement
   psyclone.psyir.nodes.structure_member
   psyclone.psyir.nodes.structure_reference

.. currentmodule:: psyclone.psyir.nodes


Functions
=========

- :py:func:`colored`:
  Colorize text.


.. autofunction:: colored


Classes
=======

- :py:class:`ArrayMember`:
  Node representing an access to the element(s) of an array that is a

- :py:class:`ArrayReference`:
  Node representing a reference to an element or elements of an Array.

- :py:class:`ArrayOfStructuresMember`:
  Node representing a membership expression of a parent structure where the

- :py:class:`ArrayOfStructuresReference`:
  Node representing an access to a member of one or more elements of an

- :py:class:`Assignment`:
  Node representing an Assignment statement. As such it has a LHS and RHS

- :py:class:`BinaryOperation`:
  Node representing a BinaryOperation expression. As such it has two operands

- :py:class:`Call`:
  Node representing a Call. This can be found as a standalone statement

- :py:class:`Clause`:
  Base abstract class for all clauses.

- :py:class:`CodeBlock`:
  Node representing some generic Fortran code that PSyclone does not

- :py:class:`Container`:
  Node representing a set of Routine and/or Container nodes, as well

- :py:class:`DataNode`:
  Abstract node representing a general PSyIR expression that represents a

- :py:class:`FileContainer`:
  PSyIR node to encapsulate the scope of a source file. In the

- :py:class:`IfBlock`:
  Node representing an if-block within the PSyIR. It has two mandatory

- :py:class:`Literal`:
  Node representing a Literal. The value and datatype properties of

- :py:class:`Loop`:
  Node representing a loop within the PSyIR. It has 4 mandatory children:

- :py:class:`Member`:
  Node representing a membership expression of a structure.

- :py:class:`NaryOperation`:
  Node representing a n-ary operation expression. The n operands are

- :py:class:`Node`:
  Base class for a PSyIR node.

- :py:class:`Operation`:
  Abstract base class for PSyIR nodes representing operators.

- :py:class:`Range`:
  The ``Range`` node is used to capture a range of integers via

- :py:class:`Reference`:
  Node representing a Reference Expression.

- :py:class:`Return`:
  Node representing a Return statement (subroutine break without return

- :py:class:`Routine`:
  A sub-class of a Schedule that represents a subroutine, function or

- :py:class:`Schedule`:
  Stores schedule information for a sequence of statements (supplied

- :py:class:`Statement`:
  Abstract node representing a general PSyIR Statement.

- :py:class:`StructureMember`:
  Node representing a membership expression of the parent's Reference that

- :py:class:`StructureReference`:
  Node representing a reference to a component of a structure. As such

- :py:class:`UnaryOperation`:
  Node representing a UnaryOperation expression. As such it has one operand

- :py:class:`ScopingNode`:
  Abstract node that has an associated Symbol Table to keep track of

- :py:class:`KernelSchedule`:
  A KernelSchedule is the parent node of the PSyIR for Kernel source code.

- :py:class:`PSyDataNode`:
  This class can be inserted into a schedule to instrument a set of nodes.

- :py:class:`ExtractNode`:
  This class can be inserted into a Schedule to mark Nodes for     code extraction using the ExtractRegionTrans transformation. By     applying the transformation the Nodes marked for extraction become     children of (the Schedule of) an ExtractNode.

- :py:class:`ProfileNode`:
  This class can be inserted into a schedule to create profiling code.

- :py:class:`NanTestNode`:
  This class can be inserted into a Schedule to mark Nodes for

- :py:class:`ReadOnlyVerifyNode`:
  This class can be inserted into a Schedule to mark Nodes for

- :py:class:`Directive`:
  Abstract base class for all Directive statements.

- :py:class:`RegionDirective`:
  Base class for all Directive nodes that have an associated

- :py:class:`StandaloneDirective`:
  Base class for all StandaloneDirective statements. This class is

- :py:class:`ACCDirective`:
  Base mixin class for all OpenACC directive statements.

- :py:class:`ACCRegionDirective`:
  Base class for all OpenACC region directive statements. 

- :py:class:`ACCStandaloneDirective`:
  Base class for all standalone OpenACC directive statements. 

- :py:class:`ACCDataDirective`:
  Class representing the !$ACC DATA ... !$ACC END DATA directive

- :py:class:`ACCEnterDataDirective`:
  Class representing a "!$ACC enter data" OpenACC directive in

- :py:class:`ACCParallelDirective`:
  Class representing the !$ACC PARALLEL directive of OpenACC

- :py:class:`ACCLoopDirective`:
  Class managing the creation of a '!$acc loop' OpenACC directive.

- :py:class:`ACCKernelsDirective`:
  Class representing the !$ACC KERNELS directive in the PSyIR.

- :py:class:`ACCUpdateDirective`:
  Class representing the !$ACC UPDATE directive of OpenACC in the PSyIR.

- :py:class:`ACCRoutineDirective`:
  Class representing a "!$ACC routine" OpenACC directive in PSyIR. 

- :py:class:`OMPDirective`:
  Base mixin class for all OpenMP-related directives.

- :py:class:`OMPRegionDirective`:
  Base class for all OpenMP region-related directives.

- :py:class:`OMPStandaloneDirective`:
  Base class for all OpenMP-related standalone directives

- :py:class:`OMPParallelDirective`:
  Class representing an OpenMP Parallel directive. 

- :py:class:`OMPSerialDirective`:
  Abstract class representing OpenMP serial regions, e.g.

- :py:class:`OMPSingleDirective`:
  Class representing an OpenMP SINGLE directive in the PSyIR.

- :py:class:`OMPMasterDirective`:
  Class representing an OpenMP MASTER directive in the PSyclone AST.

- :py:class:`OMPTaskloopDirective`:
  Class representing an OpenMP TASKLOOP directive in the PSyIR.

- :py:class:`OMPDoDirective`:
  Class representing an OpenMP DO directive in the PSyIR.

- :py:class:`OMPParallelDoDirective`:
  Class for the !$OMP PARALLEL DO directive. This inherits from

- :py:class:`OMPTaskwaitDirective`:
  Class representing an OpenMP TASKWAIT directive in the PSyIR.

- :py:class:`OMPTargetDirective`:
  Class for the !$OMP TARGET directive that offloads the code contained

- :py:class:`OMPLoopDirective`:
  Class for the !$OMP LOOP directive that specifies that the iterations

- :py:class:`OMPDeclareTargetDirective`:
  Class representing an OpenMP Declare Target directive in the PSyIR.

- :py:class:`OMPGrainsizeClause`:
  OpenMP grainsize clause, used by OMPTaskloopDirective. Controls the

- :py:class:`OMPNogroupClause`:
  OpenMP nogroup clause, used by OMPTaskloopDirective to disable the

- :py:class:`OMPNowaitClause`:
  OpenMP nowait clause. Disable the implicit barrier at the end of the

- :py:class:`OMPNumTasksClause`:
  OpenMP numtasks clause, used by OMPTaskloopDirective. Controls the number


.. autoclass:: ArrayMember
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ArrayMember
      :parts: 1

.. autoclass:: ArrayReference
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ArrayReference
      :parts: 1

.. autoclass:: ArrayOfStructuresMember
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ArrayOfStructuresMember
      :parts: 1

.. autoclass:: ArrayOfStructuresReference
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ArrayOfStructuresReference
      :parts: 1

.. autoclass:: Assignment
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Assignment
      :parts: 1

.. autoclass:: BinaryOperation
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: BinaryOperation
      :parts: 1

.. autoclass:: Call
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Call
      :parts: 1

.. autoclass:: Clause
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Clause
      :parts: 1

.. autoclass:: CodeBlock
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: CodeBlock
      :parts: 1

.. autoclass:: Container
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Container
      :parts: 1

.. autoclass:: DataNode
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DataNode
      :parts: 1

.. autoclass:: FileContainer
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: FileContainer
      :parts: 1

.. autoclass:: IfBlock
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: IfBlock
      :parts: 1

.. autoclass:: Literal
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Literal
      :parts: 1

.. autoclass:: Loop
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Loop
      :parts: 1

.. autoclass:: Member
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Member
      :parts: 1

.. autoclass:: NaryOperation
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: NaryOperation
      :parts: 1

.. autoclass:: Node
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Node
      :parts: 1

.. autoclass:: Operation
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Operation
      :parts: 1

.. autoclass:: Range
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Range
      :parts: 1

.. autoclass:: Reference
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Reference
      :parts: 1

.. autoclass:: Return
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Return
      :parts: 1

.. autoclass:: Routine
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Routine
      :parts: 1

.. autoclass:: Schedule
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Schedule
      :parts: 1

.. autoclass:: Statement
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Statement
      :parts: 1

.. autoclass:: StructureMember
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: StructureMember
      :parts: 1

.. autoclass:: StructureReference
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: StructureReference
      :parts: 1

.. autoclass:: UnaryOperation
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: UnaryOperation
      :parts: 1

.. autoclass:: ScopingNode
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ScopingNode
      :parts: 1

.. autoclass:: KernelSchedule
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: KernelSchedule
      :parts: 1

.. autoclass:: PSyDataNode
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: PSyDataNode
      :parts: 1

.. autoclass:: ExtractNode
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ExtractNode
      :parts: 1

.. autoclass:: ProfileNode
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ProfileNode
      :parts: 1

.. autoclass:: NanTestNode
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: NanTestNode
      :parts: 1

.. autoclass:: ReadOnlyVerifyNode
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ReadOnlyVerifyNode
      :parts: 1

.. autoclass:: Directive
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Directive
      :parts: 1

.. autoclass:: RegionDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: RegionDirective
      :parts: 1

.. autoclass:: StandaloneDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: StandaloneDirective
      :parts: 1

.. autoclass:: ACCDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCDirective
      :parts: 1

.. autoclass:: ACCRegionDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCRegionDirective
      :parts: 1

.. autoclass:: ACCStandaloneDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCStandaloneDirective
      :parts: 1

.. autoclass:: ACCDataDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCDataDirective
      :parts: 1

.. autoclass:: ACCEnterDataDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCEnterDataDirective
      :parts: 1

.. autoclass:: ACCParallelDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCParallelDirective
      :parts: 1

.. autoclass:: ACCLoopDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCLoopDirective
      :parts: 1

.. autoclass:: ACCKernelsDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCKernelsDirective
      :parts: 1

.. autoclass:: ACCUpdateDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCUpdateDirective
      :parts: 1

.. autoclass:: ACCRoutineDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCRoutineDirective
      :parts: 1

.. autoclass:: OMPDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPDirective
      :parts: 1

.. autoclass:: OMPRegionDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPRegionDirective
      :parts: 1

.. autoclass:: OMPStandaloneDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPStandaloneDirective
      :parts: 1

.. autoclass:: OMPParallelDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPParallelDirective
      :parts: 1

.. autoclass:: OMPSerialDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPSerialDirective
      :parts: 1

.. autoclass:: OMPSingleDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPSingleDirective
      :parts: 1

.. autoclass:: OMPMasterDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPMasterDirective
      :parts: 1

.. autoclass:: OMPTaskloopDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPTaskloopDirective
      :parts: 1

.. autoclass:: OMPDoDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPDoDirective
      :parts: 1

.. autoclass:: OMPParallelDoDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPParallelDoDirective
      :parts: 1

.. autoclass:: OMPTaskwaitDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPTaskwaitDirective
      :parts: 1

.. autoclass:: OMPTargetDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPTargetDirective
      :parts: 1

.. autoclass:: OMPLoopDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPLoopDirective
      :parts: 1

.. autoclass:: OMPDeclareTargetDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPDeclareTargetDirective
      :parts: 1

.. autoclass:: OMPGrainsizeClause
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPGrainsizeClause
      :parts: 1

.. autoclass:: OMPNogroupClause
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPNogroupClause
      :parts: 1

.. autoclass:: OMPNowaitClause
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPNowaitClause
      :parts: 1

.. autoclass:: OMPNumTasksClause
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPNumTasksClause
      :parts: 1
