import React, { useState } from "react";
import { DragDropContext, Droppable, Draggable } from "@hello-pangea/dnd";
import { PlusCircle, BookOpen, X } from "lucide-react";

export default function Board() {
  const [lists, setLists] = useState([]);
  const [newCardInput, setNewCardInput] = useState({});
  const [showListModal, setShowListModal] = useState(false);
  const [newListName, setNewListName] = useState("");

  const addList = () => {
    if (!newListName.trim()) return;

    const newId = `${lists.length + 1}`;
    setLists([...lists, { id: newId, title: newListName, cards: [] }]);

    setNewListName("");
    setShowListModal(false);
  };

  const removeList = (listId) => {
    setLists(lists.filter((list) => list.id !== listId));
  };

  const saveCard = (listId, cardName) => {
    if (!cardName.trim()) return;

    setLists(
      lists.map((list) =>
        list.id === listId
          ? {
              ...list,
              cards: [
                ...list.cards,
                { id: `c${Date.now()}`, name: cardName, done: false },
              ],
            }
          : list
      )
    );

    setNewCardInput({ ...newCardInput, [listId]: "" });
  };

  const toggleDone = (listId, cardId) => {
    setLists(
      lists.map((list) =>
        list.id === listId
          ? {
              ...list,
              cards: list.cards.map((c) =>
                c.id === cardId ? { ...c, done: !c.done } : c
              ),
            }
          : list
      )
    );
  };

  const removeCard = (listId, cardId) => {
    setLists(
      lists.map((list) =>
        list.id === listId
          ? { ...list, cards: list.cards.filter((c) => c.id !== cardId) }
          : list
      )
    );
  };

  const onDragEnd = (result) => {
    const { source, destination } = result;
    if (!destination) return;

    if (source.droppableId === destination.droppableId) {
      const list = lists.find((l) => l.id === source.droppableId);
      const reordered = Array.from(list.cards);
      const [moved] = reordered.splice(source.index, 1);
      reordered.splice(destination.index, 0, moved);

      setLists(
        lists.map((l) =>
          l.id === list.id ? { ...l, cards: reordered } : l
        )
      );
    } else {
      const sourceList = lists.find((l) => l.id === source.droppableId);
      const destList = lists.find((l) => l.id === destination.droppableId);

      const sourceCards = Array.from(sourceList.cards);
      const [moved] = sourceCards.splice(source.index, 1);

      const destCards = Array.from(destList.cards);
      destCards.splice(destination.index, 0, moved);

      setLists(
        lists.map((l) =>
          l.id === sourceList.id
            ? { ...l, cards: sourceCards }
            : l.id === destList.id
            ? { ...l, cards: destCards }
            : l
        )
      );
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 text-gray-800 p-6">
      {/* Header */}
      <div className="flex items-center justify-between bg-white shadow-md rounded-xl px-6 py-4 mb-8">
        <div className="flex gap-6 items-center">
          <h1 className="text-xl font-bold">Board Name</h1>
          <span className="text-sm text-gray-500">Created: 2025-09-28</span>
          <span className="text-sm text-gray-500">Last Updated: 2025-09-28</span>
        </div>
      </div>

      {/* Board Content */}
      <DragDropContext onDragEnd={onDragEnd}>
        <div className="flex gap-6 overflow-x-auto">
          {lists.map((list) => (
            <Droppable key={list.id} droppableId={list.id}>
              {(provided) => (
                <div
                  ref={provided.innerRef}
                  {...provided.droppableProps}
                  className="bg-white rounded-2xl shadow-lg p-4 w-64 flex-shrink-0"
                >
                  {/* List Header */}
                  <div className="flex justify-between items-center mb-4">
                    <h2 className="font-semibold text-lg">{list.title}</h2>
                    <button
                      onClick={() => removeList(list.id)}
                      className="text-gray-500 hover:text-red-500"
                    >
                      <X size={18} />
                    </button>
                  </div>

                  {/* Cards */}
                  <div className="space-y-3">
                    {list.cards.map((card, index) => (
                      <Draggable key={card.id} draggableId={card.id} index={index}>
                        {(provided) => (
                          <div
                            ref={provided.innerRef}
                            {...provided.draggableProps}
                            {...provided.dragHandleProps}
                            className="group flex items-center justify-between bg-gray-50 p-3 rounded-lg shadow-sm"
                          >
                            <div className="flex items-center gap-3">
                              <button
                                onClick={() => toggleDone(list.id, card.id)}
                                className={`w-5 h-5 rounded-full border-2 flex items-center justify-center opacity-0 group-hover:opacity-100 transition ${
                                  card.done
                                    ? "bg-green-500 border-green-500"
                                    : "border-gray-400"
                                }`}
                              />
                              <span
                                className={`text-sm ${
                                  card.done ? "line-through text-gray-400" : ""
                                }`}
                              >
                                {card.name}
                              </span>
                            </div>
                            <div className="flex gap-2">
                              <button className="text-gray-500 hover:text-indigo-600">
                                <BookOpen size={18} />
                              </button>
                              <button
                                onClick={() => removeCard(list.id, card.id)}
                                className="text-gray-400 hover:text-red-500"
                              >
                                <X size={16} />
                              </button>
                            </div>
                          </div>
                        )}
                      </Draggable>
                    ))}
                    {provided.placeholder}
                  </div>

                  {/* Inline Input for Adding Card */}
                  {newCardInput[list.id] !== undefined ? (
                    <div className="mt-3 flex gap-2">
                      <input
                        type="text"
                        autoFocus
                        value={newCardInput[list.id]}
                        onChange={(e) =>
                          setNewCardInput({ ...newCardInput, [list.id]: e.target.value })
                        }
                        onKeyDown={(e) => {
                          if (e.key === "Enter") saveCard(list.id, newCardInput[list.id]);
                          if (e.key === "Escape")
                            setNewCardInput({ ...newCardInput, [list.id]: undefined });
                        }}
                        placeholder="Enter card name..."
                        className="flex-1 border rounded-lg px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
                      />
                      <button
                        onClick={() => saveCard(list.id, newCardInput[list.id])}
                        className="px-3 py-1 bg-indigo-500 text-white text-sm rounded-lg"
                      >
                        Add
                      </button>
                    </div>
                  ) : (
                    <button
                      onClick={() => setNewCardInput({ ...newCardInput, [list.id]: "" })}
                      className="mt-4 w-full bg-indigo-100 hover:bg-indigo-200 text-indigo-700 py-2 rounded-lg font-medium"
                    >
                      + Add Card
                    </button>
                  )}
                </div>
              )}
            </Droppable>
          ))}

          {/* Add More List / Add List */}
          {/* Add More List / Add List */}
<div className="relative">
  <div
    onClick={() => setShowListModal(true)}
    className="bg-gray-200 hover:bg-gray-300 cursor-pointer rounded-2xl w-64 h-32 flex items-center justify-center flex-col text-gray-600 font-medium shadow-inner"
  >
    <PlusCircle size={28} />
    <button className="mt-2">
      {lists.length === 0 ? "Add List" : "Add More Lists"}
    </button>
  </div>

  {showListModal && (
    <>
      {/* Black overlay */}
      <div
        className="fixed inset-0 bg-white bg-opacity-40"
        onClick={() => setShowListModal(false)}
      />

      {/* Inline popup (anchored to button) */}
      <div className="absolute top-0 left-0 bg-white shadow-xl rounded-xl w-64 p-4 z-10">
        <h2 className="text-sm font-semibold mb-2">Enter List Name</h2>
        <input
          type="text"
          value={newListName}
          onChange={(e) => setNewListName(e.target.value)}
          placeholder="e.g. To Do"
          className="w-full border px-3 py-2 rounded-lg mb-3 focus:outline-none focus:ring-2 focus:ring-indigo-400"
        />
        <div className="flex justify-end gap-2">
          <button
            onClick={() => setShowListModal(false)}
            className="px-3 py-1 bg-gray-200 rounded-lg text-sm"
          >
            Cancel
          </button>
          <button
            onClick={addList}
            className="px-3 py-1 bg-indigo-500 text-white rounded-lg text-sm"
          >
            Add
          </button>
        </div>
      </div>
    </>
  )}
</div>

        </div>
      </DragDropContext>

      {/* Modal for List Name */}
      {showListModal && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-40">
          <div className="bg-white p-6 rounded-xl shadow-lg w-96">
            <h2 className="text-lg font-semibold mb-4">Enter List Name</h2>
            <input
              type="text"
              value={newListName}
              onChange={(e) => setNewListName(e.target.value)}
              placeholder="e.g. To Do, In Progress..."
              className="w-full border px-3 py-2 rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-indigo-400"
            />
            <div className="flex justify-end gap-3">
              <button
                onClick={() => setShowListModal(false)}
                className="px-4 py-2 bg-gray-200 rounded-lg"
              >
                Cancel
              </button>
              <button
                onClick={addList}
                className="px-4 py-2 bg-indigo-500 text-white rounded-lg"
              >
                Add
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
