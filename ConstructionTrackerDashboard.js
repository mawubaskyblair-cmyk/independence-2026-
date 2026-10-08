/**
 * Construction Tracker & Creator Portal Dashboard Engine
 */

class Milestone {
  constructor(id, name, estimatedDays, cost) {
    this.id = id;
    this.name = name;
    this.estimatedDays = estimatedDays;
    this.cost = cost;
    this.isCompleted = false;
    this.completionDate = null;
  }

  complete() {
    this.isCompleted = true;
    this.completionDate = new Date().toISOString().split('T')[0];
  }
}

class ConstructionProject {
  constructor(projectName, clientName, totalBudget) {
    this.projectName = projectName;
    this.clientName = clientName;
    this.totalBudget = totalBudget;
    this.milestones = [];
    this.mediaUpdates = [];
  }

  addMilestone(id, name, days, cost) {
    const milestone = new Milestone(id, name, days, cost);
    this.milestones.push(milestone);
  }

  markMilestoneComplete(id) {
    const milestone = this.milestones.find(m => m.id === id);
    if (!milestone) {
      throw new Error(`Milestone with ID ${id} was not found.`);
    }
    milestone.complete();
  }

  calculateSpentBudget() {
    return this.milestones
      .filter(m => m.isCompleted)
      .reduce((sum, m) => sum + m.cost, 0);
  }

  calculateProgressPercentage() {
    if (this.milestones.length === 0) return 0;
    const completedCount = this.milestones.filter(m => m.isCompleted).length;
    return ((completedCount / this.milestones.length) * 100).toFixed(2);
  }

  attachMediaUpdate(mediaUrl, mediaType, caption) {
    const update = {
      id: `MEDIA-${Date.now()}`,
      timestamp: new Date().toISOString(),
      mediaUrl,
      mediaType,
      caption,
      progressAtUpload: `${this.calculateProgressPercentage()}%`
    };
    this.mediaUpdates.push(update);
    return update;
  }

  generateCreatorOverlayWidget() {
    const progress = this.calculateProgressPercentage();
    const spent = this.calculateSpentBudget();
    
    return {
      title: this.projectName,
      progressBarText: `Construction Progress: ${progress}%`,
      financialSummary: `Budget Used: $${spent.toLocaleString()} / $${this.totalBudget.toLocaleString()}`,
      latestUpdate: this.mediaUpdates.length > 0 ? this.mediaUpdates[this.mediaUpdates.length - 1] : null,
      statusBadge: progress === "100.00" ? "READY FOR OCCUPANCY" : "UNDER CONSTRUCTION"
    };
  }

  generateFullSummaryReport() {
    return {
      project: this.projectName,
      client: this.clientName,
      totalBudget: this.totalBudget,
      spentBudget: this.calculateSpentBudget(),
      remainingBudget: this.totalBudget - this.calculateSpentBudget(),
      overallProgressPercentage: `${this.calculateProgressPercentage()}%`,
      milestones: this.milestones.map(m => ({
        name: m.name,
        status: m.isCompleted ? `Completed on ${m.completionDate}` : "In Progress / Pending",
        allocatedCost: m.cost
      })),
      totalMediaUploaded: this.mediaUpdates.length
    };
  }
}

// Example Execution
const project = new ConstructionProject("Grand Horizon Apartments", "Apex Developers", 1500000);

project.addMilestone(1, "Site Preparation & Excavation", 14, 120000);
project.addMilestone(2, "Foundation & Basement Pouring", 30, 350000);
project.addMilestone(3, "Steel Framing & Concrete Columns", 45, 400000);
project.addMilestone(4, "Interior Plumbing & Electrical", 25, 200000);

project.markMilestoneComplete(1);
project.markMilestoneComplete(2);

project.attachMediaUpdate("https://media.site/video_frame1.mp4", "video", "Foundation pouring completed smoothly!");

console.log("--- CREATOR OVERLAY WIDGET DATA ---");
console.log(project.generateCreatorOverlayWidget());

console.log("\n--- FULL SUMMARY REPORT ---");
console.log(JSON.stringify(project.generateFullSummaryReport(), null, 2));